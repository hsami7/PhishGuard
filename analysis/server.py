import sys
import os
import grpc
from concurrent import futures
import logging
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from protos import analyzer_pb2
from protos import analyzer_pb2_grpc
from analysis.heuristics import EmailAnalyzer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalysisService(analyzer_pb2_grpc.AnalysisServiceServicer):
    def __init__(self):
        self.analyzer = EmailAnalyzer()

    def AnalyzeEmail(self, request, context):
        logger.info(f"Received analysis request for sender: {request.sender}")

        urls_list = list(request.urls)
        result = self.analyzer.analyze(
            sender=request.sender,
            subject=request.subject,
            text_content=request.text_content,
            urls=urls_list
        )

        response = analyzer_pb2.AnalyzeResponse(
            category=result["category"],
            score_level=result["score_level"],
            numeric_score=result["numeric_score"],
            justification=result["justification"],
            explanation_json=json.dumps(result["explanation"]),
            explanation_text=result["explanation_text"],
        )
        logger.info(f"Analysis complete - Sender: {request.sender} | Category: {result['category']} | Score: {result['numeric_score']} ({result['score_level']})")
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analyzer_pb2_grpc.add_AnalysisServiceServicer_to_server(AnalysisService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("AnalysisService gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
