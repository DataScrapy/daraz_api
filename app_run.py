from flask import Flask, render_template, request, jsonify
import page_content_api
import page_status_api
from database_crud import page_content_get, page_url_status_get


app = Flask(__name__)


@app.route('/page_data/set/', methods=['GET'])
def page_data_set():
    try:
        try:
            query_parameters = request.args
            scrap_url = query_parameters.get('url')
            crawl_message = page_content_api.scrap(scrap_url)
            return crawl_message

        except Exception as e:
            return ({
                "status": "error",
                "data" : str(e)
                    })

    except Exception as e:
        return ({
            "status": "error",
            "data": str(e)
        })
        pass


@app.route('/page_data/get/', methods=['GET'])
def page_data_get():
    try:
        try:
            query_parameters = request.args
            id = query_parameters.get('task_id')

            try:
                id = int(id)
            except:
                return ({
                    "status": "error",
                    "data": "task_id must be an integer type"
                })

            crawl_message = page_content_get(id)
            return crawl_message

        except Exception as e:
            return ({
                "status": "error",
                "data" : str(e)
                    })

    except Exception as e:
        return ({
            "status": "error",
            "data": str(e)
        })
        pass


@app.route('/crawl/set/', methods=['GET'])
def crawl_set():
    try:
        try:
            query_parameters = request.args
            crawler_url = query_parameters.get('url')
            crawl_message = page_status_api.scrap(crawler_url)
            return crawl_message

        except Exception as e:
            return ({
                "status": "error",
                "data" : str(e)
                    })

    except Exception as e:
        return ({
            "status": "error",
            "data": str(e)
        })
        pass


@app.route('/crawl/get/', methods=['GET'])
def crawl_get():
    try:
        try:
            query_parameters = request.args
            id = query_parameters.get('task_id')
            try:
                id = int(id)
            except:
                return ({
                    "status": "error",
                    "data": "task_id must be an integer type"
                })

            crawl_message = page_url_status_get(id)
            return crawl_message

        except Exception as e:
            return ({
                "status": "error",
                "data" : str(e)
                    })

    except Exception as e:
        return ({
            "status": "error",
            "data": str(e)
        })
        pass



if __name__ == '__main__':
    app.run(debug=True)