import pkg_resources

requirement = pkg_resources.Requirement.parse('AnalysisEngine')
distribution = pkg_resources.working_set.find(requirement)

__version__ = distribution.version if distribution else 'N/A'
