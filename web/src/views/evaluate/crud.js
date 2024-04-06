export const crudOptions = (vm) => {
    return {

        pageOptions: {
            compact: true
        },
        options: {
            tableType: 'vxe-table',
            rowKey: true, // 必须设置，true or false
            rowId: 'id',
            height: '100%', // 表格高度100%, 使用toolbar必须设置
            highlightCurrentRow: false,
        },
        rowHandle: {
            width: 140,
            view: {
                thin: true,
                text: '',
                disabled() {
                    return !vm.hasPermissions('Retrieve')
                }
            },
            edit: {
                thin: true,
                text: '',
                disabled() {
                    return !vm.hasPermissions('Update')
                }
            },
            remove: {
                thin: true,
                text: '',
                disabled() {
                    return !vm.hasPermissions('Delete')
                }
            }

        },
        indexRow: { // 或者直接传true,不显示title，不居中
            title: '序号',
            align: 'center',
            width: 100
        },
        viewOptions: {
            componentType: 'form'
        },
        formOptions: {
            defaultSpan: 24, // 默认的表单 span
            width: '35%'
        },
        columns: [{
            title: '关键词',
            key: 'search',
            show: false,
            disabled: true,
            search: {
                disabled: false
            },
            form: {
                disabled: true,
                component: {
                    props: {
                        clearable: true
                    },
                    placeholder: '请输入关键词'
                }
            },
            view: { // 查看对话框组件的单独配置
                disabled: true
            }
        },
        {
            title: 'ID',
            key: 'id',
            show: false,
            disabled: true,
            width: 90,
            form: {
                disabled: true
            }
        },
        {
            title: '工作名称',
            key: 'job.job_name',
            // sortable: true,
            form:{
                editDisabled:true
            },
            search: {
                disabled: false,
                component: {
                    props: {
                        clearable: false
                    }
                }
            }
        },
        {
            title: '合作公司',
            key: 'job.dept_name',
            // sortable: true,
            form:{
                editDisabled:true
            }
        },
        {
            title: '合同状态',
            key: 'evaluate_status',
            type: 'select',
            dict: {
                data: vm.dictionary('evaluate_status')
            },
            form: {
                // show: false,
                // value: 0,
                component: {
                    span: 30
                }
            },
        },
        {
            title: '评分',
            key: 'mark',
            type: 'rate',
            form: {
                itemProps: {
                    class: { yxtInput: true }
                },
            }
        },
        {
            title: '工作时间',
            key: 'job.job_datetime',

            type: 'datetime',
            form: {
                editDisabled: true,
                addDisabled: true
            }
        },
        {
            title: '工作地点',
            key: 'job.job_address',
            type: 'input',
            form: {
                editDisabled: true,
                addDisabled: true,
                
            }
        },
        {
            title: '工作类型',
            key: 'job.job_type',
            type: 'select',
            dict: {
                data: vm.dictionary('job_type')
            },
            form: {
                editDisabled: true,
                addDisabled: true
            },
        },
        {
            title: '工期',
            key: 'job.duration',
            form: {
                editDisabled: true,
                addDisabled: true
            }
        },
        {
            title: '预算',
            key: 'job.wage',
            form: {
                editDisabled: true,
                addDisabled: true
            }
        },
        {
            title: '技能资质要求',
            key: 'job.job_demand',
            type: 'input',
            form: {
                editDisabled: true,
                addDisabled: true
            }
        }

        ].concat(vm.commonEndColumns())
    }
}

