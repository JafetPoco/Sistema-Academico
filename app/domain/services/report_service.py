from domain.services.reports_implementation import ReportsImplementation

class ReportService:
    def __init__(self):
        self.reports_implementation = ReportsImplementation()

    def get_course_grades_report(self, course_identifier: int):
        """Returns a report with students' grades for the given course."""
        return self.reports_implementation.get_course_grades_report(course_identifier)

