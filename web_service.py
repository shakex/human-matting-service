from fastapi import FastAPI

if __name__ == '__main__':
    uvicorn.run(app='human_matting_api:app', host='localhost', port=8008, reload=True)