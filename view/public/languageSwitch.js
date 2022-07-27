/* 0 英语 1 中文 */
const sw = 0
const lan = {
    /* 视图标题 */
    'view1': ['Statistical View', 'Statistical View'],
    'view2': ['Abstraction View', 'Abstraction View'],
    'view3': ['River View', 'River View'],
    'view4': ['Time-frequency View', 'Time-frequency View'],
    'view5': ['Setting', 'Setting'],
    'view6': ['Map', 'Map'],
    'view7': ['Signal List', 'Signal List'],
    /* 右侧设置 从上到下 */
    'set1': ['Signal Distribution Resettings', '信号分布模式'],
    'set2': ['Smart distribution', '智能分布模式'],
    'set3': ['Equidistant distribution', '等距分布模式'],
    'set4': ['Original distribution', '原始分布模式'],
    'set5': ['Display all signals', '单屏显示全部信号'],
    'set6': ['Frequency axis resolution', '频率轴分辨率'],
    'set8': ['Signal Strength', 'Signal Strength'],

}
const isTu = false
let viewSW = 1  //实验所用
viewSW = isTu ? 4 : viewSW
// 宽度 高度 左侧宽度 标题高度 左侧刷子高度
const viewPx = [
    [1270, 717, 1020, 30, 130],//1280*720
    [1910, 880, 1660, 30, 130],//1K
    [1910 * 2, 1077 * 2, 1660 * 2, 30 * 2, 130 * 2],//4K
    [1910, 1077, 1400, 30, 100],//paper word
    [1910, 1239.775, 1551.53, 30, 50],//tu word
]