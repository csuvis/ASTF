export default {
  freRange: [1290, 1295],  //这是默认一重频率范围
  extentTimeRange: ['2020-09-21 11:00:27', '2020-09-21 12:27:51'],
  extentFreRange: [1290, 1326],
  //medium        #35b6dd     #6fcbe6 
  gradColor: ['#8cd6eb', '#6fcbe6', "#52c1e2", '#35b6dd', '#23a6cd'],
  /* 视图间隔 */
  viewInter: 10,
  riverMulti: 20,

  dataInitBrushRange: [
    {             //8/03 06:00
      'timeRange': [new Date('2018-06-03 10:00:00'), new Date('2018-06-03 12:05:00')],
      'freqRange': [431.5, 439.5],
    },
    {       //8/03 06:00
      'timeRange': [new Date('2019-08-03 06:00:00'), new Date('2019-08-03 12:04:00')],
      'freqRange': [430.5, 437.8],
    }
  ]
}
