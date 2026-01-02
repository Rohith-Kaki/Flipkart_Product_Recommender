from flask import render_template, Flask, Response, request
from prometheus_client import Counter, generate_latest
from flipkart.data_ingestion import DataIngestion
from flipkart.rag_chain import RagChainBuilder
from dotenv import load_dotenv
load_dotenv()

#prometheus -> custom metric, generate_latest -> in-built metrics from promethteus
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests")

def create_app():
    app = Flask(__name__)
    vector_store = DataIngestion().ingest(load_existing=True) #already VectorDB is created.
    rag_chain = RagChainBuilder(vector_store).build_chain()

    @app.route('/')
    def index():
        REQUEST_COUNT.inc()
        return render_template('index.html')
    
    @app.route('/get', methods=["POST"])
    def get_response():
        user_input = request.form['msg']
        response = rag_chain.invoke(
            {"input": user_input},
            config={"configurable" : {"session_id": "user_session"}}
        )["answer"]
        return response
    @app.route("/metrics")
    def metrics():
       #"generate_latest exposes the inbuilt and custom metrics"
        return Response(generate_latest(), mimetype='text/plain')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)