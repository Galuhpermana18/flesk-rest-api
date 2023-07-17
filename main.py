from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, inputs
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class PesertaModel(db.Model):
	no = db.Column(db.Integer, primary_key=True)
	tglPendaftaran = db.Column(db.DateTime, nullable=False)
	nama = db.Column(db.String(100), nullable=False)
	alamat = db.Column(db.String(200))
	telp = db.Column(db.String(20))
	jenisKelamin = db.Column(db.String(10), nullable=False)
	jenisKursus = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return f""

peserta_put_args = reqparse.RequestParser()
peserta_put_args.add_argument("tglPendaftaran", type=inputs.date, help="Tanggal Pendaftaran Harus Diisi", required=True)
peserta_put_args.add_argument("nama", type=str, help="Nama Peserta Harus Diisi", required=True)
peserta_put_args.add_argument("alamat", type=str, help="Alamat Peserta")
peserta_put_args.add_argument("telp", type=str, help="Nomor Telepon Peserta")
peserta_put_args.add_argument("jenisKelamin", type=str, help="Jenis Kelamin Harus Diisi", required=True)
peserta_put_args.add_argument("jenisKursus", type=str, help="Jenis Kursus Harus Diisi", required=True)

peserta_update_args = reqparse.RequestParser()
peserta_update_args.add_argument("tglPendaftaran", type=inputs.date, help="Tanggal Pendaftaran")
peserta_update_args.add_argument("nama", type=str, help="Nama Peserta")
peserta_update_args.add_argument("alamat", type=str, help="Alamat Peserta")
peserta_update_args.add_argument("telp", type=str, help="Nomor Telepon Peserta")
peserta_update_args.add_argument("jenisKelamin", type=str, help="Jenis Kelamin Harus Diisi")
peserta_update_args.add_argument("jenisKursus", type=str, help="Jenis Kursus Harus Diisi")



class MyDateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')

resource_fields = {
	'no' : fields.Integer,
	'tglPendaftaran' : fields.DateTime,
	'nama' : fields.String,
	'alamat' : fields.String,
	'telp' : fields.String,
	'jenisKelamin' : fields.String,
	'jenisKursus' : fields.String
}

class getAll(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = PesertaModel.query.all()
		if not result:
			abort(404, message="Data Peserta Kosong")
		return result
	
class getData(Resource):
	@marshal_with(resource_fields)
	def get(self, noPeserta):
		result = PesertaModel.query.filter_by(no=noPeserta).first()
		if not result:
			abort(404, message="Nomor Peserta Tidak Ditemukan")
		return result

class insert(Resource):
	@marshal_with(resource_fields)
	def put(self, noPeserta):
		args = peserta_put_args.parse_args()
		result = PesertaModel.query.filter_by(no=noPeserta).first()
		if result:
			abort(409, message="Nomor Peserta Sudah Ada...")

		peserta = PesertaModel(
						no=noPeserta, 
						tglPendaftaran=args['tglPendaftaran'],
						nama=args['nama'],
						alamat=args['alamat'],
						telp=args['telp'],
						jenisKelamin=args['jenisKelamin'],
						jenisKursus=args['jenisKursus'],
						)
		db.session.add(peserta)
		db.session.commit()
		return peserta, 201

class update(Resource):
	@marshal_with(resource_fields)
	def patch(self, noPeserta):
		args = peserta_update_args.parse_args()
		result = PesertaModel.query.filter_by(no=noPeserta).first()
		if not result:
			abort(404, message="Nomor Peserta Tidak Ditemukan")

		if args['tglPendaftaran']:
			result.tglPendaftaran = args['tglPendaftaran']
		if args['nama']:
			result.nama = args['nama']
		if args['alamat']:
			result.alamat = args['alamat']
		if args['telp']:
			result.telp = args['telp']
		if args['jenisKelamin']:
			result.jenisKelamin = args['jenisKelamin']
		if args['jenisKursus']:
			result.jenisKursus = args['jenisKursus']
		

		db.session.commit()

		return result

class deleteAll(Resource):
	def delete(self):
		db.session.query(PesertaModel).delete()
		db.session.commit()
		return '', 204
	
class deleteData(Resource):
	def delete(self, noPeserta):
		result = PesertaModel.query.filter_by(no=noPeserta).first()
		if not result:
			abort(404, message="Nomor Peserta Tidak Ditemukan")
		db.session.delete(result)
		db.session.commit()

		return '', 204

api.add_resource(getAll, "/peserta/")
api.add_resource(getData, "/peserta/<int:noPeserta>")
api.add_resource(insert, "/peserta/insert/<int:noPeserta>")
api.add_resource(update, "/peserta/update/<int:noPeserta>")
api.add_resource(deleteAll, "/peserta/delete/")
api.add_resource(deleteData, "/peserta/delete/<int:noPeserta>")

if __name__ == "__main__":
	app.run(debug=True)