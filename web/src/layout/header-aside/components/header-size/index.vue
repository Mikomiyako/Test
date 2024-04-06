<template></template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";
export default {
  name: "d2-header-size",
  data() {
    return {
      options: [
        { label: "默认", value: "default" },
        { label: "中", value: "medium" },
        { label: "小", value: "small" },
        { label: "最小", value: "mini" },
      ],
    };
  },
  computed: {
    ...mapState("d2admin/size", ["value"]),
  },
  methods: {
    ...mapMutations({
      pageKeepAliveClean: "d2admin/page/keepAliveClean",
    }),
    ...mapActions({
      sizeSet: "d2admin/size/set",
    }),
    handleChange(value) {
      this.sizeSet(value);
      this.$notify({
        title: "提示",
        dangerouslyUseHTMLString: true,
        message:
          "已更新页面内 <b>组件</b> 的 <b>默认尺寸</b><br/>例如按钮大小，<b>非字号</b>",
        type: "success",
      });
    },
    iconName(name) {
      return name === this.value ? "dot-circle-o" : "circle-o";
    },
  },
};
</script>
