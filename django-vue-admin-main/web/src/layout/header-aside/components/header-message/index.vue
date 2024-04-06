<template></template>

<script>
import msgList from "./components/msg-list";
import { request } from "@/api/service";
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters("d2admin", {
      unread: "messagecenter/unread",
    }),
  },
  components: {
    msgList,
  },
  data() {
    return {
      msgObj: null,
    };
  },
  methods: {
    getList() {
      request({
        url: "/api/system/message_center/get_newest_msg/",
        method: "get",
        params: {},
      }).then((res) => {
        const { data } = res;
        this.msgObj = data;
      });
    },
  },
};
</script>
