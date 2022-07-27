
import $ from 'jquery'
export function showToolTip (aPosition, sHtml, cnt) {
    let toolTip = $("#tooltip")
    toolTip.html(sHtml)
    let height = 20 * cnt + 8
    let top = aPosition.y - 20 * cnt - 4
    toolTip.css({
        "top": top,
        "left": aPosition.x,
        "height": height + "px"
    })
    toolTip.show()
}
export function hideToolTip () {
    let toolTip = $("#tooltip")
    toolTip.hide()
}
function PrefixZero (num, n) {
    return (Array(n).join(0) + num).slice(-n)
}
export const format = (date, kind) => {
    let y = date.getFullYear()
    let m = date.getMonth() + 1
    let d = date.getDate()
    let h = date.getHours()
    h = h < 10 ? ('0' + h) : h
    let min = date.getMinutes()
    min = min < 10 ? ('0' + min) : min
    let sec = date.getSeconds()
    sec = sec < 10 ? ('0' + sec) : sec
    if (kind == 0)
        return m + "/" + d + " " + h + ':' + min + ':' + sec
    else if (kind == 1)
        return y + "-" + m + "-" + d + "  " + h + ':' + min + ':' + sec
    else
        return m + "/" + PrefixZero(d, 2) + " " + h + ':' + min
}