from datetime import datetime

from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import and_

import configmodule
from database import db
from models import Company, Shareholder, PhysicalPerson

def create_app(config=configmodule.Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    Migrate(app, db)

    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config["CORS_HEADERS"] = "Content-Type"
    api = Api(app)
    api.add_resource(SingleCompanyAPI, "/company/<int:reg_code>")
    api.add_resource(CompanyAPI, "/company/")
    api.add_resource(PhysicalPersonAPI, "/person/")
    return app


class SingleCompanyAPI(Resource):
    def get(self, reg_code):
        company = Company.query.filter_by(reg_code=str(reg_code)).first()
        if company:
            return company.json()
        return {"Error": "Company not found"}, 404

    def delete(self, reg_code):
        company = Company.query.filter_by(reg_code=str(reg_code)).first()
        if company:
            db.session.delete(company)
            db.session.commit()
            return {"Success": f"Company {reg_code} was deleted"}

        return {"Error": "Company not found"}, 404

    def put(self, reg_code):
        company = Company.query.filter_by(reg_code=str(reg_code)).first()
        if not company:
            return {"Error": "Company not found"}, 404

        response_json = request.get_json(force=True)

        try:
            shareholders = response_json["shareholders"]
        except:
            shareholders = []

        share_amount = 0
        shareholder_reg_code_error = False
        duplicate_shareholder_error = False
        shareholder_reg_codes = []
        missing_info_error = False
        shareholder_name_error = False

        for shareholder in shareholders:
            if (
                not shareholder.get("reg_code")
                or not shareholder.get("name")
                or not shareholder.get("share_amount")
            ):
                missing_info_error = True
            elif shareholder["reg_code"] in shareholder_reg_codes:
                duplicate_shareholder_error = True
            elif (
                len(shareholder["reg_code"]) != 7
                and len(shareholder["reg_code"]) != 11
                or not str(shareholder["reg_code"]).isnumeric()
            ):
                shareholder_reg_code_error = True

            elif not str(shareholder["name"]).replace(" ", "").isalpha():
                shareholder_name_error = True
            else:
                share_amount += shareholder["share_amount"]
                shareholder_reg_codes.append(shareholder["reg_code"])

        if shareholder_name_error:
            return {"Error": "Shareholder name can include only letters"}, 400
        elif missing_info_error:
            return {"Error": "Required info is missing"}, 400
        elif duplicate_shareholder_error:
            return {"Error": "Each shareholder must be unique"}, 400
        elif not shareholders:
            return {"Error": "Unable to create a company without shareholders"}, 400
        elif shareholder_reg_code_error:
            return {
                "Error": "Shareholder reg code must be 11 or 7 digits long and contain only numbers"
            }, 400
        elif share_amount < 2500:
            return {"Error": "Total share amount must be at least 2500"}, 400
        shareholders_list = []
        for shareholder in shareholders:
            print(shareholder)
            shareholders_list.append(
                Shareholder(
                    name=shareholder["name"],
                    share_amount=shareholder["share_amount"],
                    reg_code=shareholder["reg_code"],
                    founder=shareholder.get("founder", False),
                    physical_person=shareholder.get("physical_person", False),
                )
            )

        company.shareholders = shareholders_list
        db.session.commit()
        return company.json(), 201


class PhysicalPersonAPI(Resource):
    def get(self):
        q = request.args.to_dict().get("q")
        if q:
            result_persons = PhysicalPerson.query.filter(
                PhysicalPerson.reg_code.startswith(f"{q}")
            ).all()
            return {"result": [person.json() for person in result_persons]}, 200
        else:
            all_persons = PhysicalPerson.query.all()
            return {"result": [person.json() for person in all_persons]}, 200


class CompanyAPI(Resource):
    def get(self):
        q_home = request.args.to_dict().get("q_home")
        q_shareholder = request.args.to_dict().get("q_shareholder")
        if q_home:
            filtered_companies = Company.query.filter(
                Company.name.ilike(f"%{str(q_home)}%") | Company.reg_code.like(f"%{str(q_home)}%")
            ).all()
            result_list = [company.json() for company in filtered_companies]
            filtered_shareholders = Shareholder.query.filter(
                Shareholder.name.ilike(f"%{str(q_home)}%")
                | Shareholder.reg_code.ilike(f"%{str(q_home)}%")
            ).all()

            if filtered_shareholders and len(result_list) < 10:
                for shareholder in filtered_shareholders:
                    shareholder_parent = (
                        Company.query.filter_by(
                            reg_code=shareholder.parent_json()["parent_reg_code"]
                        )
                    ).first()

                    if (
                        shareholder_parent
                        and not shareholder_parent.json() in result_list
                    ):
                        result_list.append(shareholder_parent.json())
            result_list = result_list[0:10]
            return {"result": result_list}
        elif q_shareholder:
            filtered_companies = Company.query.filter(
                Company.reg_code.startswith(f"{q_shareholder}")
            ).all()
            result_list = [company.json() for company in filtered_companies]

            filtered_shareholders = Shareholder.query.filter(
                and_(
                    Shareholder.reg_code.startswith(f"{q_shareholder}"),
                    Shareholder.physical_person == False,
                )
            ).all()
            print(filtered_shareholders)
            if filtered_shareholders and len(result_list) < 10:
                for shareholder in filtered_shareholders:
                    shareholder_parent = (
                        Company.query.filter_by(
                            reg_code=shareholder.parent_json()["parent_reg_code"]
                        )
                    ).first()

                    if (
                        shareholder_parent
                        and not shareholder_parent.json() in result_list
                    ):
                        result_list.append(shareholder_parent.json())
            result_list = result_list[0:10]
            return {"result": result_list}
        else:
            all_companies = Company.query.all()
            return {"result": [company.json() for company in all_companies]}, 200


    def post(self):
        response_json = request.get_json(force=True)
        reg_code_exists = Company.query.filter_by(
            reg_code=response_json["reg_code"]
        ).first()
        name_exists = Company.query.filter_by(name=response_json["name"]).first()

        try:
            shareholders = response_json["shareholders"]
        except:
            shareholders = []

        share_amount = 0
        shareholder_reg_code_error = False
        duplicate_shareholder_error = False
        shareholder_reg_codes = []
        missing_info_error = False
        shareholder_name_error = False

        if not response_json.get("name") or not response_json.get("reg_code"):
            missing_info_error = True
        else:
            for shareholder in shareholders:
                if (
                    not shareholder.get("reg_code")
                    or not shareholder.get("name")
                    or not shareholder.get("share_amount")
                ):
                    missing_info_error = True
                elif shareholder["reg_code"] in shareholder_reg_codes:
                    duplicate_shareholder_error = True
                elif (
                    len(shareholder["reg_code"]) != 7
                    and len(shareholder["reg_code"]) != 11
                    or not str(shareholder["reg_code"]).isnumeric()
                ):
                    shareholder_reg_code_error = True

                elif not str(shareholder["name"]).replace(" ", "").isalpha():
                    shareholder_name_error = True
                else:
                    share_amount += shareholder["share_amount"]
                    shareholder_reg_codes.append(shareholder["reg_code"])

        if reg_code_exists or name_exists:
            return {"Error": "Company with this name or reg_code already exists"}, 400
        elif datetime.strptime(response_json["reg_date"], "%Y-%m-%d") > datetime.now():
            return {"Error": "Registration date cannot be in the future"}, 400
        elif shareholder_name_error:
            return {"Error": "Shareholder name can include only letters"}, 400
        elif not str(response_json["name"]).replace(" ", "").isalpha():
            return {"Error": "Company name can include only letters"}, 400
        elif missing_info_error:
            return {"Error": "Required info is missing"}, 400
        elif duplicate_shareholder_error:
            return {"Error": "Each shareholder must be unique"}, 400
        elif not shareholders:
            return {"Error": "Unable to create a company without shareholders"}, 400
        elif shareholder_reg_code_error:
            return {
                "Error": "Shareholder reg code must be 11 or 7 digits long and contain only numbers"
            }, 400
        elif share_amount < 2500:
            return {"Error": "Total share amount must be at least 2500"}, 400
        elif len(response_json["name"]) > 100 or len(response_json["name"]) < 3:
            return {"Error": "Name must be between 3 and 100 characters long."}, 400
        elif not (
            len(response_json["reg_code"]) == 7
            and str(response_json["reg_code"]).isnumeric()
        ):
            return {
                "Error": "Registration code must be 7 digits long and contain only numbers"
            }, 400

        company = Company(
            name=response_json["name"],
            reg_code=response_json["reg_code"],
            reg_date=datetime.strptime(response_json["reg_date"], "%Y-%m-%d"),
        )

        for shareholder in shareholders:
            company.shareholders.append(
                Shareholder(
                    name=shareholder["name"],
                    share_amount=shareholder["share_amount"],
                    reg_code=shareholder["reg_code"],
                    founder=shareholder.get("founder", False),
                    physical_person=shareholder.get("physical_person", False),
                )
            )
            sh_exists = PhysicalPerson.query.filter(
                PhysicalPerson.reg_code == shareholder["reg_code"]
            ).first()

            if shareholder.get("physical_person", False) and not sh_exists:
                print(shareholder)
                p = PhysicalPerson(
                    firstName=shareholder["name"].rsplit(" ", 1)[0],
                    lastName=shareholder["name"].rsplit(" ", 1)[1],
                    reg_code=shareholder["reg_code"],
                )
                db.session.add(p)
        db.session.add(company)
        db.session.commit()

        return company.json(), 201


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
