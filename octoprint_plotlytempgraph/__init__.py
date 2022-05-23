# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin


class PlotlytempgraphPlugin(octoprint.plugin.SettingsPlugin,
							octoprint.plugin.AssetPlugin,
							octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin

	def get_settings_version(self):
		return 1

	def on_settings_migrate(self, target, current):
		if current is None or current < 1:
			# Loop through name map and add new property
			name_map_new = []
			for mapping in self._settings.get(['name_map']):
				mapping["hidden"] = False
				name_map_new.append(mapping)
			self._settings.set(["name_map"], name_map_new)

	def get_settings_defaults(self):
		return {
			"max_graph_height": 0,
			"name_map": [
				#lase head
				{"identifier": "laser_temp actual", "label": "Laser Temp", "color": "#f60b0b", "hidden": False},
				{"identifier": "laser_temp target", "label": "Laser Temp Max", "color": "#f60b0b", "hidden": False},

				#Air filter
				{"identifier": "dust actual", "label": "Dust", "color": "213d9a", "hidden": False},
				{"identifier": "dust target", "label": "Dust", "color": "213d9a", "hidden": True},

				{"identifier": "pressure actual", "label": "Pressure", "color": "", "hidden": False},
				{"identifier": "pressure target", "label": "", "color": "", "hidden": True},

				{"identifier": "fan_rpm actual", "label": "Fan RPM", "color": "", "hidden": False},
				{"identifier": "fan_rpm target", "label": "chamber target", "color": "", "hidden": True},

				#compressor
				{"identifier": "pressure_compressor actual", "label": "Pressure Compressor", "color": "", "hidden": False},
				{"identifier": "pressure_compressor target", "label": "", "color": "", "hidden": True},

				{"identifier": "rpm_compressor actual", "label": "Pressure RPM", "color": "", "hidden": False},
				{"identifier": "rpm_compressor target", "label": "", "color": "", "hidden": True},
			],
			"always_show_legend": True
		}

	##~~ AssetPlugin mixin

	def get_assets(self):
		return dict(
			css=["css/spectrum.css", "css/PlotlyTempGraph.css"],
			js=["js/spectrum.js", "js/ko.colorpicker.js", "js/plotly-latest.min.js", "js/plotlytempgraph.js"]
		)

	def get_template_configs(self):
		return [
			dict(type="tab", name="Temperature", template="plotlytempgraph_tab.jinja2", replaces="temperature"),
			dict(type="settings", template="plotlytempgraph_settings.jinja2", replaces="temperature",
				 custom_bindings=False),
			dict(type="generic", template="plotlytempgraph.jinja2")
		]

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			plotlytempgraph=dict(
				displayName="Plotly Temp Graph",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_commit",
				user="Josef-MrBeam",
				branch="develop-josef",
				repo="OctoPrint-PlotlyTempGraph",
				current=self._plugin_version,
				stable_branch=dict(
					name="Stable", branch="master", comittish=["master"]
				),
				prerelease_branches=[
					dict(
						name="Release Candidate",
						branch="rc",
						comittish=["rc", "master"],
					),
					dict(
						name="Development",
						branch="develop",
						comittish=["develop", "rc", "master"],
					)
				],
				# update method: pip
				pip="https://github.com/Josef-MrBeam/OctoPrint-PlotlyTempGraph/archive/{target_version}.zip"
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
