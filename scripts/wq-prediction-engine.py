import sys
sys.path.append('../commonfiles/python')
import optparse
import logging.config
import time

def load_plugin_callback(plugin_info):
  plugin_info
  return
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
  logger = logging.getLogger(__name__)

  from yapsy.PluginManager import PluginManager

  logger.info("Log file opened.")


  plugin_dirs = options.plugin_directories.split(',')
  #plugin_dirs = (["plugins"])

  # Build the manager
  simplePluginManager = PluginManager()
  # Tell it the default place(s) where to find plugins
  simplePluginManager.setPluginPlaces(plugin_dirs)
  # Load all plugins
  simplePluginManager.locatePlugins()
  simplePluginManager.loadPlugins(callback=load_plugin_callback)
  #simplePluginManager.collectPlugins()

  plugin_proc_start = time.time()
  for plugin in simplePluginManager.getAllPlugins():
    if logger:
      logger.info("Executing plugin: %s" % (plugin.name))
    plugin.plugin_object.inititalize_plugin(ini=plugin.details.get("Core", "Ini"), name=plugin.name)
    plugin.plugin_object.start()

  #Wait for the plugings to finish up.
  if logger:
    logger.info("Waiting for plugins to complete.")
  for plugin in simplePluginManager.getAllPlugins():
    plugin.plugin_object.join()
  if logger:
    logger.info("Plugins completed in %f seconds" % (time.time() - plugin_proc_start))

    #plugin.plugin_object.run_wq_models()
  if logger:
    logger.info("Log file closed.")

if __name__ == "__main__":
  main()