
from .context import MapContext, AnalysisReport

class MEEResultParser:
    """
    Nimmt die Reports aus der MapEvaluationEngine auf und speichert sie.
    """

    def __init__(self):
        self.reports = []

    def ingest(self, map_context, rule_results):
        """
        MapContext + RuleResults einspeisen
        """
        report = AnalysisReport(map_context, rule_results)
        self.reports.append(report)

    def get_reports(self):
        """Alle Reports zurückgeben"""
        return self.reports

    def get_report_for_map(self, map_name):
        """Report einer bestimmten Map zurückgeben"""
        for r in self.reports:
            if r.map_context.map_name == map_name:
                return r
        return None
