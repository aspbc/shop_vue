import re

file_path = "/workspace/shop_vue/src/components/generated/ProductProductList.vue"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add comments to JS functions
js_stock = """// 处理 "库存" 按钮点击，打开库存管理弹窗并初始化数据
const handleStock = (row) => {
  currentStockRow.value = row
  // 模拟接口获取库存明细并装配到列表，现阶段为单规格默认结构
  stockData.value = [{
    image: row.image || 'https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=product+image&image_size=square',
    spec: '默认',
    barcode: '',
    code: '',
    currentStock: row.stock,
    changeStock: 0, // 修改的增量/减量
    changeType: 'add' // 增量操作还是减量操作：add=入库，sub=出库
  }]
  stockDialogVisible.value = true
}

// 提交库存更改请求
const submitStock = async () => {
  try {
    // 根据表格中的"加/减"逻辑计算最终库存数值
    const finalStock = getFinalStock(stockData.value[0])
    const payload = { ...currentStockRow.value, stock: finalStock }
    
    // 调用更新接口保存数据
    const res = await axios.post(`/api/admin/store/product/save`, payload)
    if (res.data.code === 200) {
      ElMessage.success('库存修改成功')
      stockDialogVisible.value = false
      fetchData() // 刷新列表
    } else {
      ElMessage.error(res.data.msg || '库存修改失败')
    }
  } catch (e) {
    ElMessage.error('网络错误')
  }
}"""
content = content.replace("""const handleStock = (row) => {
  currentStockRow.value = row
  stockData.value = [{
    image: row.image || 'https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=product+image&image_size=square',
    spec: '默认',
    barcode: '',
    code: '',
    currentStock: row.stock,
    changeStock: 0,
    changeType: 'add'
  }]
  stockDialogVisible.value = true
}

const submitStock = async () => {
  try {
    const finalStock = getFinalStock(stockData.value[0])
    const payload = { ...currentStockRow.value, stock: finalStock }
    const res = await axios.post(`/api/admin/store/product/save`, payload)
    if (res.data.code === 200) {
      ElMessage.success('库存修改成功')
      stockDialogVisible.value = false
      fetchData()
    } else {
      ElMessage.error(res.data.msg || '库存修改失败')
    }
  } catch (e) {
    ElMessage.error('网络错误')
  }
}""", js_stock)

js_stats = """// 请求获取各状态(Tab页签)的统计数据(销售中、回收站等)
// 传入当前的搜索条件(searchQuery)以保证各个页签的数字在特定搜索场景下依然精确联动
const fetchHeaderStats = async () => {
  try {
    const params = { ...searchQuery }
    const res = await axios.get('/api/admin/store/product/type_header', { params })
    if (res.data.code === 200) {
      headerStats.value = res.data.data
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}"""
content = content.replace("""const fetchHeaderStats = async () => {
  try {
    const params = { ...searchQuery }
    const res = await axios.get('/api/admin/store/product/type_header', { params })
    if (res.data.code === 200) {
      headerStats.value = res.data.data
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}""", js_stats)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
