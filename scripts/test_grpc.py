import sys
import os
import grpc

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from proto import analyzer_pb2
from proto import analyzer_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = analyzer_pb2_grpc.AnalysisServiceStub(channel)
        
        print("--- Testing Benign Email ---")
        benign_req = analyzer_pb2.EmailRequest(
            sender="alice@company.com",
            subject="Lunch tomorrow?",
            text_content="Hey, are we still on for lunch?",
            urls=["http://company.com/menu"]
        )
        response = stub.AnalyzeEmail(benign_req)
        print(f"Level: {response.score_level}")
        print(f"Score: {response.numeric_score}")
        print(f"Justification: {response.justification}\n")

        print("--- Testing Phishing Email ---")
        phish_req = analyzer_pb2.EmailRequest(
            sender="admin@192.168.1.1",
            subject="URGENT: Action Required for your account",
            text_content="Dear Customer, your password will expire. Click here to verify.",
            urls=["http://192.168.1.1/login"]
        )
        response = stub.AnalyzeEmail(phish_req)
        print(f"Level: {response.score_level}")
        print(f"Score: {response.numeric_score}")
        print(f"Justification: {response.justification}")

if __name__ == '__main__':
    run()
