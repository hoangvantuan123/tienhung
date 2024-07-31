/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, useRef, onMounted } = owl

export class PerformanceDashboard extends Component {
    setup(){

    }
}

PerformanceDashboard.template = "dash.PerformanceDashboard"
PerformanceDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add("dash.performance_dashboard", PerformanceDashboard)