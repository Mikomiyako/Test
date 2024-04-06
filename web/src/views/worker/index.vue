<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @deliveryWork="deliveryWork"
    >
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
          v-if="tabActivted === 'job'"
        />
        <!-- <el-button-group>
            <el-button size="small" type="primary" @click="recommend_job"
              > 智能推荐工作</el-button
            >
          </el-button-group> -->
        <el-tabs v-model="tabActivted" @tab-click="onTabClick">
          <el-tab-pane label="已发布的工作" name="job"></el-tab-pane>
          <el-tab-pane label="智能推荐工作" name="recommendJob"></el-tab-pane>
        </el-tabs>
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from "./api";
import { crudOptions } from "./crud";
import { d2CrudPlus } from "d2-crud-plus";
export default {
  name: "job",
  mixins: [d2CrudPlus.crud],
  data() {
    return {
      evaluateObj: {},
      tabActivted: "job",
      role_flag: false,
    };
  },
  methods: {
    getCrudOptions() {
      const flag = api.get_user_info().then((res) => {
        if (res.code === 2000) {
          const role_info = res.data.role_info;
          this.role_flag = role_info.some((role) => role.key === "worker");
        }
      });
      return crudOptions(this);
    },
    pageRequest(query) {
      if (this.tabActivted === "recommendJob") {
        return api.recommend_job({ ...query });
      } else {
        return api.GetList(query);
      }
    },
    addRequest(row) {
      d2CrudPlus.util.dict.clear();
      return api.createObj(row);
    },
    updateRequest(row) {
      d2CrudPlus.util.dict.clear();
      return api.UpdateObj(row);
    },
    delRequest(row) {
      return api.DelObj(row.id);
    },
    // 授权
    createPermission(scope) {
      this.$router.push({
        name: "menuButton",
        params: { id: scope.row.id },
        query: { name: scope.row.name },
      });
    },
    deliveryWork(row) {
      this.evaluateObj = {
        job: row.row.id,
        evaluate_status: 0,
      };
      return api.createEvaluateObj(this.evaluateObj).then((res) => {
        if (res.code === 2000) {
          this.$message.success("投递完成");
        } else {
          this.$message.error("投递失败");
        }
      });
    },
    onTabClick(tab) {
      const { name } = tab;
      this.tabActivted = name;
      this.doRefresh();
    },
  },
};
</script>

<style lang="scss">
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}
</style>
