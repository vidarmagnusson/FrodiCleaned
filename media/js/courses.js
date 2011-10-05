
fields = ["course", "descriptive_name", "level", "subjects", "topics", "credits", "description", "prerequisites"]

function notification(text) {
	alert(text);
}

function course_save() {
	$(".course_save").text("Saving...");
	course = {};
	for (f in fields) {
		course[fields[f]] = $("#id_" + fields[f]).val();
	}

	$.post("/programmes/courses/save/", course, function(data) {
		$(".course_save").text("Save");
		if (data.ok) {
			$(".course_status").text(data.status);
			$(".course_lastsaved").html(data.course.modification_date + "<br/>ID: " + data.course.id + "<br/>Version: " + data.course.version);
			$("#id_course").val(data.course.id);
		} else {
			notification("Saving failed.");
		}
	}, "json");
	
}
