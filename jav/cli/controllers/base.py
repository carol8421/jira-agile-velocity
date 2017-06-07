"""Jira Agile Velocity base controller."""

from cement.ext.ext_argparse import ArgparseController, expose

from jav.core.javRun import Run
from jav.core.javSetup import Setup
from jav.core.javClear import Clear
from jav.core.javChart import Chart
from jav.core.javCrunch import Crunch
from jav.core.javLoad import Load
from jav.core.javConfig import Config
from jav.core.javLogConfig import LogConfig

class javBaseController(ArgparseController):

    class Meta:
        label = 'base'
        description = 'Connect to Jira REST API to collect completed story points, calculate weekly velocity, and estimate completion date'
        arguments = [
            (
                ['-d', '--dry-run'],
                dict(help='Do not send message to slack', action='store_true')
            )
        ]

    @expose(help='Clear previous data (USE WITH CAUTION)')
    def clear(self):
        clear = Clear(self.app.log, self.app.config)
        clear.main()

    @expose(help='Enter setup mode and provide configuration parameters (jira creds, slack details)')
    def setup(self):
        setup = Setup(self.app.log, self.app.config)
        setup.main()

    @expose(help='Load latest data from Jira into cache')
    def load(self):
        self.config = Config(self.app.log)
        LogConfig(self.app.log, self.app.config, self.config.config_path + 'load.log')

        load = Load(self.app.log, self.app.config)
        load.refresh_jira_cache()

    @expose(help='Obtain updated data from Jira and crunch numbers')
    def crunch(self):
        self.config = Config(self.app.log)
        LogConfig(self.app.log, self.app.config, self.config.config_path + 'crunch.log')

        # Loading saved files into memory to be used by the component crunching numbers
        load = Load(self.app.log, self.app.config)
        daily_data, remaining_work = load.load_jira_cache()

        crunch = Crunch(self.app.log, self.config)
        crunch.crunch_stats(daily_data, remaining_work)

    @expose(help='Create charts from cached data')
    def chart(self):
        self.config = Config(self.app.log)
        LogConfig(self.app.log, self.app.config, self.config.config_path + 'chart.log')

        chart = Chart(self.app.log, self.app.config)
        chart.main()

    @expose(help='Get data, crunch numbers, do stuff')
    def run(self):
        self.config = Config(self.app.log)
        LogConfig(self.app.log, self.app.config, self.config.config_path + 'run.log')

        # Load data from Jira
        load = Load(self.app.log, self.app.config)
        daily_data, remaining_work = load.refresh_jira_cache()

        # Crunch numbers
        crunch = Crunch(self.app.log, self.config)
        crunch.main(daily_data, remaining_work)

        #run = Run(self.app.log, self.app.pargs.dry_run, self.app.config)
        #run.main()









