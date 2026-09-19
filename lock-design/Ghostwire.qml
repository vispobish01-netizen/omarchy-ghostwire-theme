// Ghostwire.qml — custom lock design for the SirJul1337 Lock Screen Explorer plugin
// (Omarchy 4 / Quattro). Drop this file into ~/.config/omarchy/lock-designs/
// (or use `omarchy-shell lock rescanDesigns` after copying it there).
//
// Built against the documented DesignBase contract (README.md of
// SirJul1337/omarchy-lock-explorer): passwordText, failureMessage,
// failedAttempts, authenticatingPassword, fingerprintConfigured,
// inputEnabled, now, userName, hostName, greeting().
// NOT yet verified against a live Quattro shell — if `omarchy plugin validate`
// / qmllint flags a property mismatch, check the current designs/*.qml files
// shipped in the plugin (e.g. Zen.qml) for the exact base-class API on your
// installed version and adjust property names accordingly.

import QtQuick
import Quickshell
import "../plugins/io.github.sirjul1337.lock-explorer/designs"

DesignBase {
    id: root
    shakeOnFail: true
    showPasswordToggle: false

    // Ghostwire palette
    readonly property color bg: "#08090d"
    readonly property color fg: "#c8d2e6"
    readonly property color dim: "#3a4250"
    readonly property color cyan: "#50dcc8"
    readonly property color purple: "#9664dc"
    readonly property color red: "#dc5050"

    Wallpaper {
        anchors.fill: parent
        blurred: true
    }

    Rectangle {
        anchors.fill: parent
        color: Qt.rgba(0.05, 0.06, 0.09, 0.35)
    }

    // ============= glitch offset driver =============
    QtObject {
        id: glitch
        property bool flickerOn: true
        property bool cutOn: false
        property bool corruptOn: false
        property bool scrambleOn: false
    }

    Timer { interval: 80;  running: true; repeat: true; onTriggered: glitch.flickerOn  = Math.random() > 0.5 }
    Timer { interval: 100; running: true; repeat: true; onTriggered: glitch.cutOn      = Math.random() < 0.25 }
    Timer { interval: 150; running: true; repeat: true; onTriggered: glitch.corruptOn  = Math.random() < 0.16 }
    Timer { interval: 90;  running: true; repeat: true; onTriggered: glitch.scrambleOn = Math.random() < 0.2  }

    function hhmmss() {
        return Qt.formatTime(root.now, "hh:mm:ss")
    }
    function scrambled() {
        return hhmmss().replace(/[0-9]/g, "#")
    }
    function cut5() {
        return hhmmss().substring(0, 5)
    }

    Item {
        anchors.centerIn: parent
        width: 400
        height: 200

        // purple ghost, left offset
        Text {
            text: hhmmss()
            color: Qt.rgba(0.59, 0.39, 0.86, 0.5)
            font.pixelSize: 48
            font.family: "JetBrainsMono Nerd Font"
            anchors.centerIn: parent
            x: parent.width / 2 - width / 2 - 3
        }

        // cyan flicker, right offset
        Text {
            visible: glitch.flickerOn
            text: hhmmss()
            color: Qt.rgba(0.31, 0.86, 0.78, 0.35)
            font.pixelSize: 48
            font.family: "JetBrainsMono Nerd Font"
            anchors.centerIn: parent
            x: parent.width / 2 - width / 2 + 3
        }

        // soft top ghost
        Text {
            text: hhmmss()
            color: Qt.rgba(0.78, 0.82, 0.90, 0.1)
            font.pixelSize: 48
            font.family: "JetBrainsMono Nerd Font"
            anchors.centerIn: parent
            y: parent.height / 2 - height / 2 - 2
        }

        // red cut glitch
        Text {
            visible: glitch.cutOn
            text: cut5()
            color: Qt.rgba(0.86, 0.31, 0.31, 0.4)
            font.pixelSize: 48
            font.family: "JetBrainsMono Nerd Font"
            anchors.centerIn: parent
        }

        // hard corruption
        Text {
            visible: glitch.corruptOn
            text: "88:88:88"
            color: Qt.rgba(0.78, 0.82, 0.90, 0.5)
            font.pixelSize: 48
            font.family: "JetBrainsMono Nerd Font"
            anchors.centerIn: parent
        }

        // number scramble, cyan
        Text {
            visible: glitch.scrambleOn
            text: scrambled()
            color: Qt.rgba(0.31, 0.86, 0.78, 0.35)
            font.pixelSize: 48
            font.family: "JetBrainsMono Nerd Font"
            anchors.centerIn: parent
        }

        // main clock
        Text {
            text: hhmmss()
            color: Qt.rgba(0.78, 0.82, 0.90, 0.95)
            font.pixelSize: 48
            font.family: "JetBrainsMono Nerd Font"
            anchors.centerIn: parent
            style: Text.Raised
            styleColor: Qt.rgba(0, 0, 0, 0.8)
        }
    }

    Text {
        text: root.userName
        color: Qt.rgba(0.78, 0.82, 0.90, 0.35)
        font.pixelSize: 18
        font.family: "JetBrainsMono Nerd Font"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.verticalCenter
        anchors.topMargin: 150
    }

    Text {
        text: "state: you are not here"
        color: Qt.rgba(0.31, 0.86, 0.78, 0.28)
        font.pixelSize: 13
        font.family: "JetBrainsMono Nerd Font"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.verticalCenter
        anchors.topMargin: 185
    }

    PasswordField {
        id: pw
        inputItem: pw
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.verticalCenter
        anchors.topMargin: 230
    }
}
