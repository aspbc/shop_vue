<template>
  <div class="product-list-container">
    <el-card shadow="never" class="table-card">
      
      <!-- 1. 商品状态多页签 -->
      <el-tabs v-model="searchQuery.type" @tab-click="handleTabClick" class="status-tabs">
        <el-tab-pane v-for="item in headerStats" :key="item.type" :name="item.type.toString()">
          <template #label>
            {{ item.name }} ({{ item.count }})
          </template>
        </el-tab-pane>
      </el-tabs>


      <!-- 2. 多维搜索参数区域 -->
      <div class="search-wrapper">
        <el-form :inline="true" :model="searchQuery" class="advanced-search-form" size="default">
          <el-row :gutter="15">
            <el-col :span="6">
              <el-form-item label="商品搜索" style="width: 100%;">
                <el-input v-model="searchQuery.keyword" placeholder="请输入关键字" class="input-with-select">
                  <template #prepend>
                    <el-select v-model="searchQuery.field_key" style="width: 100px;">
                      <el-option label="名称" value="store_name" />
                      <el-option label="商品ID" value="product_id" />
                      <el-option label="关键字" value="keyword" />
                    </el-select>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="商品类型" style="width: 100%;">
                <el-select v-model="searchQuery.product_type" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="普通商品" value="0" />
                  <el-option label="卡密" value="1" />
                  <el-option label="优惠券" value="2" />
                  <el-option label="虚拟商品" value="3" />
                  <el-option label="次卡商品" value="4" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="商品分类" style="width: 100%;">
                <el-select v-model="searchQuery.cate_id" placeholder="全部分类" clearable style="width: 100%;">
                  <el-option label="手机数码" value="1" />
                  <el-option label="家用电器" value="2" />
                  <el-option label="服装服饰" value="3" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="配送方式" style="width: 100%;">
                <el-select v-model="searchQuery.delivery_type" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="快递" value="1" />
                  <el-option label="门店自提" value="2" />
                  <el-option label="门店配送" value="3" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6" class="text-right">
              <el-form-item style="margin-right: 0;">
                <el-button type="primary" @click="fetchData" :icon="Search">搜索</el-button>
                <el-button @click="resetSearch">重置</el-button>
                <el-button type="primary" link @click="isExpandSearch = !isExpandSearch">
                  {{ isExpandSearch ? '收起' : '高级搜索' }}
                  <el-icon><ArrowDown v-if="!isExpandSearch" /><ArrowUp v-else /></el-icon>
                </el-button>
              </el-form-item>
            </el-col>
          </el-row>
          
          <!-- 高级搜索展开部分 -->
          <el-row :gutter="15" v-show="isExpandSearch" style="margin-top: 15px;">
            <el-col :span="4">
              <el-form-item label="商品规格" style="width: 100%;">
                <el-select v-model="searchQuery.spec_type" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="单规格" value="0" />
                  <el-option label="多规格" value="1" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="销量区间" style="width: 100%;">
                <div class="range-input">
                  <el-input v-model="searchQuery.sales_min" placeholder="最低" style="width: 45%;" />
                  <span style="margin: 0 5px;">-</span>
                  <el-input v-model="searchQuery.sales_max" placeholder="最高" style="width: 45%;" />
                </div>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="售价区间" style="width: 100%;">
                <div class="range-input">
                  <el-input v-model="searchQuery.price_min" placeholder="最低" style="width: 45%;" />
                  <span style="margin: 0 5px;">-</span>
                  <el-input v-model="searchQuery.price_max" placeholder="最高" style="width: 45%;" />
                </div>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>

      
      
      <!-- 3. 操作按钮 -->
      <div class="action-bar" style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
        <div class="left-actions">
          
          <el-button type="success" @click="handleAction('collect')" plain>商品采集</el-button>
          
          <el-button type="warning" @click="handleBatchStatus(1)" v-if="searchQuery.type === '2'">批量上架</el-button>
          <el-button type="warning" @click="handleBatchStatus(2)" v-if="searchQuery.type === '1'">批量下架</el-button>
          <el-button type="danger" @click="handleBatchStatus(6)" v-if="searchQuery.type !== '6'" plain>移入回收站</el-button>
          <el-button type="danger" @click="handleBatchDelete" v-if="searchQuery.type === '6'">彻底删除</el-button>
          
          <el-button type="primary" @click="handleAction('batchSet')" plain>批量设置</el-button>
          <el-button type="info" @click="handleAction('migrate')" plain>商品迁移</el-button>
          <el-button type="info" @click="handleExport" plain>导出数据</el-button>
        </div>
        <div class="right-actions">
          <el-checkbox v-model="isAll" :true-label="1" :false-label="0" @change="handleSelectAllChange">跨页全选</el-checkbox>
        </div>
      </div>



      <!-- 4. 商品数据表格 -->
      <el-table :data="tableData" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange" border>
        <el-table-column type="selection" width="50" align="center" />
        <el-table-column prop="id" label="商品ID" width="80" align="center" />
        <el-table-column label="商品图" width="80" align="center">
          <template #default="scope">
            <el-image 
              style="width: 40px; height: 40px; border-radius: 4px;"
              :src="'https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=product+image&image_size=square'" 
              fit="cover"
            />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="商品名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="price" label="商品售价" width="100" align="center">
          <template #default="scope">
            <span style="color: #f5222d; font-weight: bold;">¥{{ scope.row.price || '99.00' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="sales" label="销量" width="80" align="center">
          <template #default="scope">
            {{ scope.row.sales || Math.floor(Math.random() * 1000) }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="80" align="center">
          <template #default="scope">
            {{ scope.row.stock || Math.floor(Math.random() * 500) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="scope">
            <el-switch 
              v-model="scope.row.status" 
              :active-value="1" 
              :inactive-value="0" 
              @change="handleStatusChange(scope.row)" 
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right" align="center">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="primary" link @click="handleDetail(scope.row)">查看详情</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div style="margin-top: 20px; display: flex; justify-content: flex-end;">
        <el-pagination 
          background 
          layout="total, sizes, prev, pager, next, jumper" 
          :total="total" 
          :page-sizes="[10, 20, 50, 100]"
          v-model:current-page="searchQuery.page"
          v-model:page-size="searchQuery.limit"
          @current-change="fetchData"
          @size-change="fetchData"
        />
      </div>
    </el-card>

    <!-- 添加/编辑商品对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="650px">
      <el-form label-width="100px" :model="form" ref="formRef">
        <el-form-item label="商品名称" required>
          <el-input v-model="form.name" placeholder="请输入商品名称"></el-input>
        </el-form-item>
        <el-row>
          <el-col :span="12">
            <el-form-item label="售价">
              <el-input-number v-model="form.price" :precision="2" :step="1" :min="0" style="width: 100%;" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="库存">
              <el-input-number v-model="form.stock" :min="0" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="上架状态">
          <el-switch v-model="form.status" :active-value="1" :inactive-value="0" active-text="上架" inactive-text="下架" />
        </el-form-item>
        <el-form-item label="商品备注">
          <el-input type="textarea" v-model="form.remark" placeholder="请输入内部备注"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog title="商品详情" v-model="detailVisible" width="500px">
      <el-descriptions border :column="1">
        <el-descriptions-item label="ID">{{ detailData.id }}</el-descriptions-item>
        <el-descriptions-item label="商品名称">{{ detailData.name }}</el-descriptions-item>
        <el-descriptions-item label="售价">¥ {{ detailData.price || '99.00' }}</el-descriptions-item>
        <el-descriptions-item label="库存">{{ detailData.stock || 100 }} 件</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="detailData.status === 1 ? 'success' : 'danger'">{{ detailData.status === 1 ? '出售中' : '仓库中' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailData.createTime || '2024-05-18 12:00:00' }}</el-descriptions-item>
        <el-descriptions-item label="备注">{{ detailData.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, ArrowDown, ArrowUp } from '@element-plus/icons-vue'

const axios = inject('axios')
const tableData = ref([])
const total = ref(0)
const loading = ref(false)

const dialogVisible = ref(false)
const dialogTitle = ref('新增商品')
const detailVisible = ref(false)
const detailData = ref({})
const selectedRows = ref([])
const isExpandSearch = ref(false)

const headerStats = ref([])
const isAll = ref(0) // 0:当页 1:跨页全选

const handleSelectAllChange = (val) => {
  if (val === 1) {
    ElMessage.success(`已开启跨页全选 (当前状态下共 ${total.value} 件商品)`)
  } else {
    ElMessage.info('已取消跨页全选')
  }
}


const fetchHeaderStats = async () => {
  try {
    const res = await axios.get('/api/admin/extend/product_product_list/type_header')
    if (res.data.code === 200) {
      headerStats.value = res.data.data
    }
  } catch (error) {
    console.error('获取头部统计失败')
  }
}

const handleAction = (type) => {
  if (type === 'collect') ElMessage.success('打开商品采集界面...')
  if (type === 'batchSet') {
    if (selectedRows.value.length === 0) return ElMessage.warning('请选择商品')
    ElMessage.success('打开批量设置界面...')
  }
  if (type === 'migrate') ElMessage.success('打开商品迁移向导...')
}

const handleBatchStatus = (targetStatus) => {
  if (selectedRows.value.length === 0) return ElMessage.warning('请选择要操作的商品')
  
  const actionName = targetStatus === 1 ? '上架' : (targetStatus === 2 ? '下架' : '移入回收站')
  ElMessageBox.confirm(`确认将选中的 ${selectedRows.value.length} 个商品${actionName}吗?`, '提示', { type: 'warning' })
    .then(async () => {
      try {
        const ids = selectedRows.value.map(item => item.id)
        const res = await axios.post(`/api/admin/extend/product_product_list/batch_status`, { ids, status: targetStatus })
        if (res.data.code === 200) {
          ElMessage.success(`批量${actionName}成功`)
          fetchData()
  fetchHeaderStats()
          fetchHeaderStats()
        }
      } catch(e) {
        ElMessage.error('网络错误')
      }
    }).catch(() => {})
}


const searchQuery = reactive({
  type: '1', // 默认 出售中
  field_key: 'store_name',
  keyword: '',
  product_type: '',
  cate_id: '',
  delivery_type: '',
  spec_type: '',
  sales_min: '',
  sales_max: '',
  price_min: '',
  price_max: '',
  page: 1,
  limit: 20
})

const form = reactive({
  id: null,
  name: '',
  price: 99.00,
  stock: 100,
  status: 1,
  remark: ''
})

const handleTabClick = (tab) => {
  searchQuery.page = 1
  fetchData()
  fetchHeaderStats()
}


const fetchData = async () => {
  loading.value = true
  try {
    const params = { ...searchQuery }
    const res = await axios.get('/api/admin/extend/product_product_list/list', { params })
    if (res.data.code === 200) {
      tableData.value = res.data.data.records || res.data.data
      total.value = res.data.total || tableData.value.length
    } else {
      ElMessage.error(res.data.msg || '获取数据失败')
    }
  } catch (error) {
    if (!error.response || error.response.status !== 401) {
      ElMessage.error('获取列表失败')
    }
  } finally {
    loading.value = false
  }
}


const resetSearch = () => {
  searchQuery.field_key = 'store_name'
  searchQuery.keyword = ''
  searchQuery.product_type = ''
  searchQuery.cate_id = ''
  searchQuery.delivery_type = ''
  searchQuery.spec_type = ''
  searchQuery.sales_min = ''
  searchQuery.sales_max = ''
  searchQuery.price_min = ''
  searchQuery.price_max = ''
  searchQuery.page = 1
  fetchData()
  fetchHeaderStats()
}

const handleSelectionChange = (val) => {
  selectedRows.value = val
}

const handleAdd = () => {
  dialogTitle.value = '添加商品'
  form.id = null
  form.name = ''
  form.price = 99.00
  form.stock = 100
  form.status = 1
  form.remark = ''
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑商品'
  form.id = row.id
  form.name = row.name
  form.price = row.price || 99.00
  form.stock = row.stock || 100
  form.status = row.status
  form.remark = row.remark || ''
  dialogVisible.value = true
}

const handleDetail = async (row) => {
  try {
    const res = await axios.get(`/api/admin/extend/product_product_list/detail?id=${row.id}`)
    if (res.data.code === 200) {
      detailData.value = res.data.data
    } else {
      detailData.value = { ...row }
    }
  } catch(e) {
    detailData.value = { ...row }
  }
  detailVisible.value = true
}

const handleStatusChange = async (row) => {
  try {
    const res = await axios.post(`/api/admin/extend/product_product_list/save`, row)
    if (res.data.code === 200) {
      ElMessage.success('商品状态已修改')
      // 重新拉取以刷新不同 Tab 页的数据
      fetchData()
  fetchHeaderStats()
    } else {
      ElMessage.error(res.data.msg || '状态修改失败')
    }
  } catch(e) {
    ElMessage.error('网络错误')
  }
}



const handleDelete = (row) => {
  ElMessageBox.confirm('确认将该商品移入回收站吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      const res = await axios.post(`/api/admin/extend/product_product_list/batch_status`, { ids: [row.id], status: 6 })
      if (res.data.code === 200) {
        ElMessage.success('已移入回收站')
        fetchData()
        fetchHeaderStats()
      }
    } catch(e) {
      ElMessage.error('网络错误')
    }
  }).catch(() => {})
}

const handleBatchDelete = () => {
  if (selectedRows.value.length === 0) return ElMessage.warning('请选择要删除的商品')
  ElMessageBox.confirm(`确认将选中的 ${selectedRows.value.length} 个商品移入回收站吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    const ids = selectedRows.value.map(item => item.id)
    try {
      const res = await axios.post(`/api/admin/extend/product_product_list/delete`, { ids })
      if (res.data.code === 200) {
        ElMessage.success('批量删除成功')
        fetchData()
  fetchHeaderStats()
      } else {
        ElMessage.error(res.data.msg || '删除失败')
      }
    } catch(e) {
      ElMessage.error('网络错误')
    }
  }).catch(() => {})
}

const handleExport = async () => {
  ElMessage.success('开始导出商品数据...')
  // mock export
  setTimeout(() => {
    ElMessage.success('导出完成')
  }, 1000)
}

const submitForm = async () => {
  try {
    const res = await axios.post(`/api/admin/extend/product_product_list/save`, form)
    if (res.data.code === 200) {
      ElMessage.success(form.id ? '编辑成功' : '添加成功')
      dialogVisible.value = false
      fetchData()
  fetchHeaderStats()
    } else {
      ElMessage.error(res.data.msg || '保存失败')
    }
  } catch(e) {
    ElMessage.error('网络错误')
  }
}

onMounted(() => {
  fetchData()
  fetchHeaderStats()
})
</script>

<style scoped>
.product-list-container {
  background-color: #f0f2f5;
  min-height: 100%;
}
.table-card {
  border-radius: 4px;
  border: none;
}
.search-wrapper {
  background-color: #f8f8f9;
  padding: 15px 15px 0;
  margin-bottom: 15px;
  border-radius: 4px;
}
.status-tabs {
  margin-bottom: 10px;
}
:deep(.el-tabs__nav-wrap::after) {
  height: 1px;
}
.range-input {
  display: flex;
  align-items: center;
}
.text-right {
  text-align: right;
}
</style>
