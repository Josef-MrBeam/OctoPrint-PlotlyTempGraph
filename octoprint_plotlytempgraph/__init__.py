# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class PlotlytempgraphPlugin(octoprint.plugin.SettingsPlugin,
                            octoprint.plugin.AssetPlugin,
                            octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		return dict(
			js=["js/plotly-latest.min.js","js/plotlytempgraph.js"]
		)

	def get_template_configs(self):
		return [
			dict(type="tab", name="Temperature", template="plotlytempgraph_tab.jinja2", replaces="temperature"),
			dict(type="settings", template="plotlytempgraph_settings.jinja2", replaces="temperature", custom_bindings=False),
			dict(type="generic", template="plotlytempgraph.jinja2")
		]

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			plotlytempgraph=dict(
				displayName="Plotly Temp Graph",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="jneilliii",
				repo="OctoPrint-PlotlyTempGraph",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/jneilliii/OctoPrint-PlotlyTempGraph/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "Plotly Temp Graph"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PlotlytempgraphPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

