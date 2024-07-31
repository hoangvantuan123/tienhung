/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import { TableHome } from "./table_home/table_home"
import { CardMe } from "./card_me/card_me"
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks"
import { CardUserCoutOnl, CardUserCoutOff} from "./card_user_cout/card_user_cout"
import { Blog } from "./blog/blog"
import { New } from "./new/new"

const { Component, onWillStart, useRef, onMounted, useState } = owl
export class Home extends Component {
    setup(){
        this.state = useState({
            value: 1,
            userStatusCounts: { online_count: 0, offline_count: 0 }
        });

        onWillStart(async ()=>{
            this.increment()
            await this.fetchUserStatusCounts();
    
        })
    }
    increment() {
        this.state.value++;
    }
    async fetchUserStatusCounts() {
        try {
            const response = await fetch('/api/user_status_counts', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const result = await response.json();
            this.state.userStatusCounts = result;
        } catch (error) {
            this.state.userStatusCounts = { online_count: 0, offline_count: 0 };
        }
    }
}

Home.template = "x_plan.Home"
Home.components = { KpiCard, ChartRenderer , TableHome, CardMe, CardUserCoutOnl , CardUserCoutOff, Blog, New}

registry.category("actions").add("x_plan.home", Home)