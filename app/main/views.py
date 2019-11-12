import os

from flask import render_template, session, redirect, url_for, flash, current_app

from . import main
from .forms import FileForm
from .process_data import process_file
from werkzeug.utils import secure_filename

from flask import send_from_directory

@main.route("/", methods=["GET", "POST"])  # or e.g. /upload if want other home page
def index():
    form = FileForm()
    if form.validate_on_submit():
        session["data"] = dict()
        f = form.file.data
        try:
            session["file_name"] = secure_filename(f.filename)
            f_path = os.path.join("files", session["file_name"])
            f.save(f_path)  # todo: current_app.instance_path, ... instead
            
            #creates a processed file in "files"
            d = process_file(f_path)
            dpath = os.path.join("files","results_" +session["file_name"])
            d.to_csv(dpath)
            
            flash("You have uploaded a file!")
            return render_template("result_list.html", file_name=session.get("file_name"), data=d)
        except Exception as e:
            flash("Error during upload")
            raise e
            # return redirect(url_for('.index'))
    return render_template("index.html", form=form, file_name=session.get("file_name"))  # upload.html


#download function retrieves processed file from "files" and downloads it in Downloads
@main.route("/get-csv/<csv_id>")
def get_csv(csv_id):
    csv_name = "results_"+csv_id
    csv = os.path.abspath("files")

    print(csv_name)
    try:
        
        return send_from_directory(csv, filename=csv_name, as_attachment=True)
    
    except Exception as e:
            flash("Error during download")
            raise e
    
