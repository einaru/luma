CONFIG +=      qt debug

SOURCES =      luma/base/gui/AboutDialog.py \
               luma/base/gui/MainWindow.py \
               luma/base/gui/PluginSettings.py \
               luma/base/gui/ServerDelegate.py \
               luma/base/gui/ServerDialog.py \
               luma/base/gui/Settings.py \
               luma/base/gui/SettingsDialog.py \
               luma/base/gui/SplashScreen.py \
               luma/plugins/browser_plugin/item/LDAPErrorItem.py \
               luma/plugins/browser_plugin/item/LDAPTreeItem.py \
               luma/plugins/browser_plugin/item/LDAPErrorItem.py \
               luma/plugins/browser_plugin/model/LDAPTreeItemModel.py \
               luma/plugins/browser_plugin/BrowserView.py

FORMS =        resources/forms/AboutCreditsDesign.ui \
               resources/forms/AboutDialogDesign.ui \
               resources/forms/AboutLicenseDesign.ui \
               resources/forms/LoggerWidgetDesign.ui \
               resources/forms/MainWindowDesign.ui \
               resources/forms/ServerDialogDesign.ui \
               resources/forms/SettingsDialogDesign.ui \
               resources/forms/plugins/search/SearchFilterWizardDesign.ui \
               resources/forms/plugins/search/SearchFormDesign.ui

TRANSLATIONS = resources/i18n/luma_en.ts \
               resources/i18n/luma_no.ts \
               resources/i18n/luma_hx.ts

RESOURCES =    luma/resources.py
