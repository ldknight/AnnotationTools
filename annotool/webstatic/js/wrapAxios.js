// import axios from "./axios.js"
// let axios = require("./axios.js")
//线下地址
//  const root = "http://localhost:8081/textRetrievalProj_war_exploded/";
const root = "http://127.0.0.1:5000/"
//const root = "http://localhost:8080/textRetrievalProj_war_exploded/";
//线上地址
// var root = "http://localhost:8087/textRetrievalProj_war_exploded/";

const instance = axios.create({
    baseURL:root,
    timeout:5000
})
//请求拦截
instance.interceptors.request.use(
    function (config){
        config.headers.Access_Token=localStorage.getItem('_Access_Token');
        config.headers.Business_Access_Token=localStorage.getItem('_Business_Access_Token');
        return config;
    },
    function (err){
        return Promise.reject(err);
    }
)
//响应拦截
instance.interceptors.response.use(
    function (response){
        return response;
    },
    function (err){
        return Promise.reject(err);
    }
)

function axiosGet(url,params){
    return instance.get(root+url,{params});
}
function axiosPost(url,data){
    return instance.post(root+url,Qs.stringify(data));
}
function getbaseurl(){
    return root;
}