CONFIG +=      qt debug

SOURCES =      luma/base/gui/MainWin.py \
               luma/base/gui/ServerDialog.py

FORMS =        resources/forms/AboutCreditsDesign.ui \
               resources/forms/AboutDialogDesign.ui \
               resources/forms/AboutLicenseDesign.ui \
               resources/forms/LoggerWidgetDesign.ui \
               resources/forms/MainWinDesign.ui \
               resources/forms/ServerDialogDesign.ui \
               resources/forms/SettingsDialogDesign.ui

TRANSLATIONS = resources/i18n/luma_en.ts \
               resources/i18n/luma_no.ts \
               resources/i18n/luma_hx.ts

RESOURCES =    luma/resources.py
