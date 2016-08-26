import sys
sys.path.append('../../commonfiles/python')
import optparse
import logging.config
import time
from yapsy.PluginManager import PluginManager

from wq_prediction_plugin import wq_prediction_engine_plugin

def main():
  parser = optparse.OptionParser()
  parser.add_option("-l", "--LogConfigFile", dest="log_config_file",
                    help="Logging Configuration file." )
  parser.add_option("-p", "--PluginDirList", dest="plugin_directories",
                    help="Comma separated directory list to search for plugins.")
  parser.add_option("-s", "--StartDateTime", dest="start_date_time",
                    help="A date to re-run the predictions for, if not provided, the default is the current day. Format is YYYY-MM-DD HH:MM:SS." )

  (options, args) = parser.parse_args()

  if(options.plugin_directories is None):
    parser.print_help()
    sys.exit(-1)

  if options.log_config_file:
    logging.config.fileConfig(options.log_config_file)
    logging.getLogger('yapsy').setLevel(logging.DEBUG)
  logger = logging.getLogger(__name__)

  logger.info("Log file opened.")

  plugin_dirs = options.plugin_directories.split(',')
  #plugin_dirs = (["plugins"])

  # Build the manager
  simplePluginManager = PluginManager()
  # Tell it the default place(s) where to find plugins
  if logger:
    logger.debug("Plugin directories: %s" % (options.plugin_directories))

  simplePluginManager.setCategoriesFilter({
     "PredictionEngine" : wq_prediction_engine_plugin
     })
  simplePluginManager.setPluginPlaces(plugin_dirs)
  # Load all plugins
  if logger:
    logger.info("Begin loading plugins")
  simplePluginManager.collectPlugins()

  plugin_proc_start = time.time()
  cnt = 0

  for plugin in simplePluginManager.getAllPlugins():
    if logger:
      logger.info("Starting plugin: %s" % (plugin.name))
    if plugin.plugin_object.initialize_plugin(ini=plugin.details.get("Core", "Ini"), name=plugin.name):
      plugin.plugin_object.start()
    else:
      logger.error("Failed to initialize plugin: %s" % (plugin.name))
    cnt += 1

  #Wait for the plugings to finish up.
  if logger:
    logger.info("Waiting for %d plugins to complete." % (cnt))
  for plugin in simplePluginManager.getAllPlugins():
    plugin.plugin_object.join()
  if logger:
    logger.info("Plugins completed in %f seconds" % (time.time() - plugin_proc_start))

    #plugin.plugin_object.run_wq_models()

  if logger:
    logger.info("Log file closed.")

if __name__ == "__main__":
  main()