from flask import Flask, views
from flask_restful import Api, Resource, marshal_with, reqparse, abort, fields, marshal
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/database.db"
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"


# db.create_all()


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the vid is required", required=True)
video_put_args.add_argument(
    "likes", type=int, help="Likes of the vid is required", required=True)
video_put_args.add_argument(
    "views", type=int, help="Views on the vid is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="Name of the vid is required")
video_update_args.add_argument(
    "likes", type=int, help="Likes of the vid is required")
video_update_args.add_argument(
    "views", type=int, help="Views on the vid is required")

resource_field = {
    'id': fields.Integer,
    'name': fields.String,
    'likes': fields.Integer,
    'views': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_field)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id == video_id).first()
        if not result:
            abort(404, message="Could not find video with that id")
        return result

    @marshal_with(resource_field)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id == video_id).first()
        if result:
            abort(409, message="Video id already exists..")
        video = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_field)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id == video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, Can't update..")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()

        return result

    def delete(self, video_id):
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
