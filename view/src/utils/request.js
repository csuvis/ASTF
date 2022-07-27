
import axios from 'axios'
import NProgress from 'nprogress'
//import { Message } from 'element-ui';
NProgress.configure({ showSpinner: false })
const request = axios.create({
    baseURL: process.env.VUE_APP_BASE_URL,
    timeout: 120000000,
    /*
    headers: {
        'Content-Type':'application/json',
    }
    */
})
//请求拦截器，请求之前先进入请求拦截器
request.interceptors.request.use(
    config => {
        //config.headers['token'] = store.state.token
        //若请求文件 则 config.headers['Content-Type'] = "文件"
        // console.log(config)
        let str = config.url.substring(0, 13)
        if (str != "/get_Spectrum")
            NProgress.start()
        return config
    },
    error => {
        return Promise.reject(error)
    }
)
//响应拦截器，响应之前先进入响应拦截器
request.interceptors.response.use(
    response => {
        NProgress.done()
        //Message.success("数据获取成功")
        return response
    },
    error => {
        NProgress.done()
        // Message.error("这是错误的请求")
        return Promise.reject(error)
    }
)
export default request
