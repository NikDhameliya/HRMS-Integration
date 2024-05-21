odoo.define('graph_widget_ept.graph', function (require) {
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');

    var EmiproDashboardGraph = AbstractField.extend({
        className: "dashboard_graph_ept",
        events: {
            'click #perform_operation button':'_performOpration',
            'click #instance_employee': '_getEmployees',
            'click #instance_department': '_getDepartments',
            'click #instance_leave': '_getLeaves',
            'click #instance_log': '_getLog',
        },
        init: function () {
            this._super.apply(this, arguments);
            // this.data = JSON.parse(this.value);
            this.data = this.recordData
            this.match_key = _.find(_.keys(this.data), function(key){ return key.includes('_order_data') })

            this.context = this.record.context
        },
        /**
         * The widget view uses the ChartJS lib to render the graph. This lib
         * requires that the rendering is done directly into the DOM (so that it can
         * correctly compute positions). However, the views are always rendered in
         * fragments, and appended to the DOM once ready (to prevent them from
         * flickering). We here use the on_attach_callback hook, called when the
         * widget is attached to the DOM, to perform the rendering. This ensures
         * that the rendering is always done in the DOM.
         */
        on_attach_callback: function () {
            this._isInDOM = true;
            this._renderInDOM();
        },
        /**
         * Called when the field is detached from the DOM.
         */
        on_detach_callback: function () {
            this._isInDOM = false;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * Render the widget only when it is in the DOM.
         *
         * @override
         * @private
         */
        _render: function () {
            return Promise.resolve();
        },
        /**
         * Render the widget. This function assumes that it is attached to the DOM.
         *
         * @private
         */



        /*Render action for  Employees */
        _getEmployees: function () {
            return this.do_action(this.graph_data.employee_data.employee_action)
        },

        /*Render action for  Departments */
        _getDepartments: function () {
            return this.do_action(this.graph_data.department_data.department_action)
        },

        /*Render action for  Leaves */
        _getLeaves: function () {
            return this.do_action(this.graph_data.leave_data.leave_action)
        },


        /*Render(Open)  Operations wizard*/
        _performOpration: function () {
            return this._rpc({model: this.model,method: 'perform_operation',args: [this.res_id]}).then( (result) => {
                this.do_action(result)
            });
        },

        /*Render action for  Common Log Book */
        _getLog: function () {
         return this._rpc({model: this.model,method: 'open_logs',args: [this.res_id]}).then( (result) => {
                this.do_action(result)
            });
        },

    });

    fieldRegistry.add('dashboard_graph_ept', EmiproDashboardGraph);
    return {
        EmiproDashboardGraph: EmiproDashboardGraph
    };
});