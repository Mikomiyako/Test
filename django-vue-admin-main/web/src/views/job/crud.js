import { request } from "@/api/service";
import { BUTTON_STATUS_NUMBER } from "@/config/button";
import { urlPrefix as bookPrefix } from "./api";

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: "vxe-table",
      rowKey: true, // 必须设置，true or false
      rowId: "id",
      height: "100%", // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false,
    },
    rowHandle: {
      width: 140,
      view: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Retrieve");
        },
      },
      edit: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Update");
        },
      },
      remove: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Delete");
        },
      },
    },
    indexRow: {
      // 或者直接传true,不显示title，不居中
      title: "序号",
      align: "center",
      width: 100,
    },
    viewOptions: {
      componentType: "form",
    },
    formOptions: {
      defaultSpan: 24, // 默认的表单 span
      width: "35%",
    },
    columns: [
      {
        title: "关键词",
        key: "search",
        show: false,
        disabled: true,
        search: {
          disabled: false,
        },
        form: {
          disabled: true,
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入关键词",
          },
        },
        view: {
          // 查看对话框组件的单独配置
          disabled: true,
        },
      },
      {
        title: "ID",
        key: "id",
        show: false,
        disabled: true,
        width: 90,
        form: {
          disabled: true,
        },
      },
      {
        title: "发布公司",
        key: "dept_name",
        form: {
          editDisabled: true,
          addDisabled: true,
        },
      },
      {
        title: "工作名称",
        key: "job_name",
        sortable: true,

        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },

        type: "input",
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: "显示值必填项" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入显示值",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "工作时间",
        key: "job_datetime",
        sortable: true,

        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },

        type: "datetime",
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: "显示值必填项" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入工作时间",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "工作地点",
        key: "job_address",
        sortable: true,

        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },

        type: "input",
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: "显示值必填项" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入显示值",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "工作类型",
        key: "job_type",
        type: "select",
        sortable: true,
        // width: 70,
        dict: {
          data: vm.dictionary("job_type"),
        },
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: "显示值必填项" },
          ],
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "工期",
        key: "duration",
        sortable: true,

        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },

        type: "input",
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: "显示值必填项" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入显示值",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "预算",
        key: "wage",
        sortable: true,

        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },

        type: "input",
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: "显示值必填项" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入显示值",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "技能资质要求",
        key: "job_demand",
        sortable: true,

        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },

        type: "input",
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: "显示值必填项" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入显示值",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "最优报价",
        key: "job_best_offer",
        type: "input",
        show: false,
        form: {
          component: {
            props: {
              clearable: true,
            },
            placeholder: "3000", // 默认值，可据情况修改
            readOnly: true,
          },
          addDisabled: true,
          editDisabled: true,
        },
      },
    ].concat(vm.commonEndColumns()),
  };
};
