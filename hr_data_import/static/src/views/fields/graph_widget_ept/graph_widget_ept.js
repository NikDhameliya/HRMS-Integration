/** @odoo-module **/

import { loadJS } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class DashboardGraph extends Component {
    static template = "hr_data_import.DashboardGraph";
    static props = {
        ...standardFieldProps,
        graphType: String,
    };

    constructor() {
        super(...arguments);
        this.selectedOption = "";
    }

    setup() {
        super.setup();
        this.chart = null;
        this.orm = useService("orm");
        this.action = useService('action');
        this.canvasRef = useRef("canvas");
        this.rpc = useService("rpc");
        this.data = ''
        if(this.props.record.data[this.props.name]) {
            this.data = JSON.parse(this.props.record.data[this.props.name]);
        }

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        useEffect(() => {
            this.renderChart();
            return () => {
                if (this.chart) {
                    this.chart.destroy();
                }
            };
        });
    }

    /**
     * Instantiates a Chart (Chart.js lib) to render the graph according to
     * the current config.
     */
    renderChart(currentTarget) {

        $(currentTarget).parent('div').find('.ep_graph_details .col-3 > h4 span').html(this.graph_data.currency_symbol + this.graph_data.total_sales)

        $(currentTarget).parent('div').find('#instance_employee > p:first-child').html(this.graph_data.employee_data && this.graph_data.employee_data.employee_count ? this.graph_data.employee_data.employee_count: 0);
        $(currentTarget).parent('div').find('#instance_department > p:first-child').html(this.graph_data.department_data && this.graph_data.department_data.department_count ? this.graph_data.department_data.department_count : 0);
        $(currentTarget).parent('div').find('#instance_leave > p:first-child').html(this.graph_data.leave_data && this.graph_data.leave_data.leave_count ? this.graph_data.leave_data.leave_count : 0);
    }

    /*Render action for  Leaves */
    _getEmployees() {
        return this.action.doAction(this.graph_data.employee_date.employee_action);
    }

    /*Render action for  Departments */
    _getDepartments() {
        return this.action.doAction(this.graph_data.department_data.department_action);
    }

    /*Render action for Leaves */
    _getLeaves() {
        return this.action.doAction(this.graph_data.leave_data.leave_action);
    }

    _getLog() {
        var self = this;
        return this.orm.call(
            this.props.record.resModel,
            "open_logs",
            [this.props.record.resId],
        ).then(function (result) {
            self.action.doAction(result)
        })
    }

    /*Render(Open)  Operations wizard*/
    _performOpration() {
        var self = this;
        return this.orm.call(
            this.props.record.resModel,
            "perform_operation",
            [this.props.record.resId],
        ).then(function (result) {
            self.action.doAction(result)
        })
    }
}

export const emiproDashboardGraph = {
    component: DashboardGraph,
    supportedTypes: ["text"],
    extractProps: ({ attrs }) => ({
        graphType: attrs.graph_type,
    }),
};

registry.category("fields").add("dashboard_graph_ept", emiproDashboardGraph);