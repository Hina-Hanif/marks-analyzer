from django.shortcuts import render, redirect
import numpy as np

def index(request):
    # If POST: process input and save to session, then redirect (PRG pattern)
    if request.method == "POST":
        names_input = request.POST.get("names")
        marks_input = request.POST.get("marks")
        passing_marks_input = request.POST.get("passing_marks")

        try:
            names = [name.strip() for name in names_input.split(",")]
            marks_list = list(map(int, marks_input.split(",")))
            passing_marks = int(passing_marks_input)

            if len(names) != len(marks_list):
                request.session['result'] = ["❌ Names and marks count must match."]
            else:
                marks_array = np.array(marks_list)

                max_marks = marks_array.max()
                min_marks = marks_array.min()
                avg_marks = marks_array.mean()

                top_student = names[marks_list.index(max_marks)]
                low_student = names[marks_list.index(min_marks)]

                result = [
                    f"🎯 Top Student: {top_student} ({max_marks} marks)",
                    f"😞 Lowest Student: {low_student} ({min_marks} marks)",
                    f"📊 Average Marks: {avg_marks:.2f}",
                    "— Individual Scores —"
                ]

                # Individual scores
                result += [f"{n}: {m} marks" for n, m in zip(names, marks_list)]

                # Failed students
                fail_students = [f"{n} ({m} marks)" for n, m in zip(names, marks_list) if m < passing_marks]

                if fail_students:
                    result.append("— ❌ Failed Students —")
                    result += fail_students
                else:
                    result.append("✅ All students passed!")

                request.session['result'] = result

        except:
            request.session['result'] = ["❌ Please enter valid comma-separated numbers for marks."]

        return redirect('index')  # 🔁 PRG redirect

    # On GET, pop result (show only once)
    result = request.session.pop('result', None)
    return render(request, 'marks_app/index.html', {'result': result})
