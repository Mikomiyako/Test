import { request } from "@/api/service";
export const urlPrefix = "/api/system/job/";
export const urlEvaluatePrefix = "/api/system/evaluate/";

/**
 * 列表查询
 */
export function GetList(query) {
  return request({
    url: urlPrefix,
    method: "get",
    params: query,
  });
}
/**
 * 新增
 */
export function createObj(obj) {
  return request({
    url: urlPrefix,
    method: "post",
    data: obj,
  });
}

/**
 * 修改
 */
export function UpdateObj(obj) {
  return request({
    url: urlPrefix + obj.id + "/",
    method: "put",
    data: obj,
  });
}
/**
 * 删除
 */
export function DelObj(id) {
  return request({
    url: urlPrefix + id + "/",
    method: "delete",
    data: { id },
  });
}

/**
 * evaluate 薪资
 */
export function createEvaluateObj(obj) {
  return request({
    url: urlEvaluatePrefix,
    method: "post",
    data: obj,
  });
}

export function recommend_job(query) {
  return request({
    url: urlPrefix + "recommend_job",
    method: "get",
    params: query,
  });
}

export function get_user_info() {
  return request({
    url: "/api/system/user/user_info/",
    method: "get",
    params: {},
  });
}
