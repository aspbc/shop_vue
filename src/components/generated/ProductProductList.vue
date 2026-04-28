<template>
  <div class="product-list-container">
    <el-card shadow="never" class="table-card">
      <!-- 1. 商品状态多页签 -->
      <el-tabs :model-value="searchQuery.type" @update:modelValue="handleTabChange" class="status-tabs">
        <el-tab-pane :name="1">
          <template #label>销售中 ({{ headerStats.selling || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane :name="2">
          <template #label>仓库中 ({{ headerStats.warehouse || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane :name="4">
          <template #label>已售罄 ({{ headerStats.soldOut || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane :name="5">
          <template #label>库存预警 ({{ headerStats.alert || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane :name="6">
          <template #label>回收站 ({{ headerStats.recycle || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane :name="0">
          <template #label>待审核 ({{ headerStats.pending || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane :name="-1">
          <template #label>审核未通过 ({{ headerStats.rejected || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane :name="-2">
          <template #label>强制下架 ({{ headerStats.forced || 0 }})</template>
        </el-tab-pane>
      </el-tabs>

      <!-- 2. 多维搜索参数区域 -->
      <div class="search-wrapper">
        <el-form :inline="true" :model="searchQuery" class="advanced-search-form" size="default">
          <el-row :gutter="15">
            <el-col :span="6">
              <el-form-item label="商品搜索" style="width: 100%;">
                <el-input v-model="searchQuery.store_name" placeholder="商品名称/关键字/ID" clearable class="input-with-select">
                  <template #prepend>
                    <el-select v-model="searchQuery.field_key" style="width: 100px;">
                      <el-option label="全部" value="all" />
                      <el-option label="商品ID" value="product_id" />
                      <el-option label="商品名称" value="store_name" />
                    </el-select>
                  </template>
                </el-input>
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
              <el-form-item label="商品类型" style="width: 100%;">
                <el-select v-model="searchQuery.product_type" placeholder="全部" clearable style="width: 100%;">
                  <el-option label="普通商品" value="0" />
                  <el-option label="卡密" value="1" />
                  <el-option label="虚拟商品" value="3" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="10" class="text-right">
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
            <el-col :span="6">
              <el-form-item label="销量区间" style="width: 100%;">
                <div class="range-input">
                  <el-input v-model="searchQuery.salesMin" placeholder="最低" style="width: 45%;" />
                  <span style="margin: 0 5px;">-</span>
                  <el-input v-model="searchQuery.salesMax" placeholder="最高" style="width: 45%;" />
                </div>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="售价区间" style="width: 100%;">
                <div class="range-input">
                  <el-input v-model="searchQuery.priceMin" placeholder="最低" style="width: 45%;" />
                  <span style="margin: 0 5px;">-</span>
                  <el-input v-model="searchQuery.priceMax" placeholder="最高" style="width: 45%;" />
                </div>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>

      <!-- 3. 操作按钮 -->
      <div class="action-bar" style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
        <div class="left-actions">
          <el-button type="primary" @click="handleAdd">发布商品</el-button>
          <el-button type="success" plain>商品采集</el-button>
          <el-button type="warning" plain v-if="searchQuery.type === 2">批量上架</el-button>
          <el-button type="warning" plain v-if="searchQuery.type === 1">批量下架</el-button>
          <el-button type="info" @click="handleExport" plain>导出数据</el-button>
        </div>
      </div>

      <!-- 4. 商品数据表格 -->
      <el-table :data="tableData" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="expand" width="30">
          <template #default="props">
            <div style="padding: 10px 20px; background-color: #fafafa; border-radius: 4px;">
              <p>暂无更多规格详情展示。</p>
            </div>
          </template>
        </el-table-column>
        <el-table-column type="selection" width="100" align="center">
          <template #header>
            <el-dropdown trigger="hover">
              <span style="color: var(--el-color-primary); font-size: 13px; cursor: pointer; display: inline-flex; align-items: center;">
                全选({{ selectedCount }})<el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>当前页</el-dropdown-item>
                  <el-dropdown-item>所有页</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
        <el-table-column prop="id" label="商品ID" width="80" align="center" />
        <el-table-column label="商品图" width="80" align="center">
          <template #default="scope">
            <el-image
              style="width: 40px; height: 40px; border-radius: 4px;"
              :src="scope.row.image || 'https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=product+image&image_size=square'"
              fit="cover"
            />
          </template>
        </el-table-column>
        <el-table-column label="商品名称" min-width="250" show-overflow-tooltip>
          <template #default="scope">
            <span style="color: #409EFF; margin-right: 4px;">【单规格】</span>
            <span>{{ scope.row.storeName }}</span>
          </template>
        </el-table-column>
        <el-table-column label="商品来源" width="100" align="center">
          <template #default>平台</template>
        </el-table-column>
        <el-table-column label="商品类型" width="100" align="center">
          <template #default>普通商品</template>
        </el-table-column>
        <el-table-column prop="price" label="商品售价" width="100" align="center">
          <template #default="scope">
            <span>{{ scope.row.price || '0.00' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="sales" label="销量" width="80" align="center" />
        <el-table-column prop="stock" label="库存" width="80" align="center" />
        <el-table-column prop="sort" label="排序" width="80" align="center" />
        <el-table-column label="状态" width="100" align="center" v-if="searchQuery.type !== 6">
          <template #default="scope">
            <el-switch
              v-model="scope.row.isShow"
              :active-value="1"
              :inactive-value="0"
              @change="handleStatusChange(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right" align="center">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleDetail(scope.row)">详情</el-button>
            <el-button size="small" type="primary" link @click="handleEdit(scope.row)" v-if="searchQuery.type !== 6">编辑</el-button>
            <el-button size="small" type="primary" link @click="handleStock(scope.row)">库存</el-button>
            <el-dropdown trigger="click" style="margin-left: 12px; vertical-align: middle;">
              <span class="el-dropdown-link" style="color: var(--el-color-primary); font-size: 12px; cursor: pointer; display: inline-flex; align-items: center;">
                更多<el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>佣金管理</el-dropdown-item>
                  <el-dropdown-item>查看评论</el-dropdown-item>
                  <el-dropdown-item @click="handleDelete(scope.row)">移到回收站</el-dropdown-item>
                  <el-dropdown-item>商品预览</el-dropdown-item>
                  <el-dropdown-item>复制商品</el-dropdown-item>
                  <el-dropdown-item>分享商品</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
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
          <el-input v-model="form.storeName" placeholder="请输入商品名称"></el-input>
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
          <el-switch v-model="form.isShow" :active-value="1" :inactive-value="0" active-text="上架" inactive-text="下架" />
        </el-form-item>
        <el-form-item label="商品图片">
          <el-input v-model="form.image" placeholder="请输入图片URL"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 库存管理对话框 -->
    <el-dialog title="库存管理" v-model="stockDialogVisible" width="700px">
      <el-table :data="stockData" style="width: 100%" border>
        <el-table-column label="图片" width="80" align="center">
          <template #default="scope">
            <el-image style="width: 40px; height: 40px; border-radius: 4px;" :src="scope.row.image" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column prop="spec" label="产品规格" min-width="120" />
        <el-table-column prop="barcode" label="商品条形码" width="100" />
        <el-table-column prop="code" label="商品编码" width="100" />
        <el-table-column prop="currentStock" label="当前库存" width="100" align="center" />
        <el-table-column label="入/出库数量" width="220" align="center">
          <template #default="scope">
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
              <el-input-number v-model="scope.row.changeStock" :min="0" :controls="false" style="width: 60px;" />
              <el-select v-model="scope.row.changeType" style="width: 80px;">
                <el-option label="入库" value="add" />
                <el-option label="出库" value="sub" />
              </el-select>
              <span>={{ getFinalStock(scope.row) }}</span>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="stockDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitStock">提交</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 详情抽屉 -->
    <el-drawer title="商品详情" v-model="detailDrawerVisible" size="60%">
      <div class="drawer-header-info">
        <el-icon color="var(--el-color-primary)" size="24"><Goods /></el-icon>
        <span style="margin-left: 10px; font-weight: bold;">商品ID: {{ currentDetail.id }}</span>
      </div>
      <el-tabs v-model="detailActiveTab" style="margin-top: 20px;">
        <el-tab-pane label="基础信息" name="basic">
          <div class="detail-section">
            <h3 class="detail-title"><span class="title-bar"></span>基础信息</h3>
            <el-row :gutter="20" class="detail-row">
              <el-col :span="24" class="detail-item"><span class="detail-label">商品名称：</span>{{ currentDetail.storeName }}</el-col>
              <el-col :span="8" class="detail-item"><span class="detail-label">商品分类：</span>{{ currentDetail.cateName || '-' }}</el-col>
              <el-col :span="8" class="detail-item"><span class="detail-label">商品品牌：</span>{{ currentDetail.brandName || '-' }}</el-col>
              <el-col :span="8" class="detail-item"><span class="detail-label">商品单位：</span>{{ currentDetail.unitName || '-' }}</el-col>
              <el-col :span="8" class="detail-item"><span class="detail-label">商品标签：</span>{{ currentDetail.labelName || '-' }}</el-col>
              <el-col :span="8" class="detail-item"><span class="detail-label">商品编码：</span>{{ currentDetail.code || '-' }}</el-col>
            </el-row>
            <div style="margin-top: 15px;" class="detail-item">
              <span class="detail-label">商品轮播图：</span>
              <div style="display: flex; gap: 10px; margin-top: 10px;">
                <el-image v-for="(img, idx) in (currentDetail.sliderImage || [currentDetail.image])" :key="idx" :src="img" style="width: 60px; height: 60px; border-radius: 4px; border: 1px solid #eee;" fit="cover" />
              </div>
            </div>
          </div>
          
          <div class="detail-section" style="margin-top: 30px;">
            <h3 class="detail-title"><span class="title-bar"></span>物流设置</h3>
            <el-row :gutter="20" class="detail-row">
              <el-col :span="12" class="detail-item"><span class="detail-label">配送方式：</span>快递</el-col>
              <el-col :span="12" class="detail-item"><span class="detail-label">运费设置：</span>包邮</el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="规格库存" name="spec">
          <el-empty description="暂无数据" />
        </el-tab-pane>
        <el-tab-pane label="商品详情" name="content">
          <el-empty description="暂无数据" />
        </el-tab-pane>
        <el-tab-pane label="其他设置" name="other">
          <el-empty description="暂无数据" />
        </el-tab-pane>
        <el-tab-pane label="商品评论" name="reply">
          <el-empty description="暂无数据" />
        </el-tab-pane>
      </el-tabs>
    </el-drawer>
  </div>
</template>


<script setup>
import { ref, reactive, onMounted, inject, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, ArrowDown, ArrowUp, Goods } from '@element-plus/icons-vue'

const axios = inject('axios')
const tableData = ref([])
const total = ref(0)
const loading = ref(false)

const dialogVisible = ref(false)
const dialogTitle = ref('发布商品')
const isExpandSearch = ref(false)

const headerStats = ref({
  selling: 0,
  warehouse: 0,
  soldOut: 0,
  alert: 0,
  recycle: 0,
  pending: 0,
  rejected: 0,
  forced: 0
})

const selectedCount = ref(0)
const handleSelectionChange = (val) => {
  selectedCount.value = val.length
}


const stockDialogVisible = ref(false)
const stockData = ref([])
const currentStockRow = ref(null)

const getFinalStock = (row) => {
  const change = row.changeStock || 0
  if (row.changeType === 'add') {
    return row.currentStock + change
  } else {
    return Math.max(0, row.currentStock - change)
  }
}

// 处理 "库存" 按钮点击，打开库存管理弹窗并初始化数据
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
}

const detailDrawerVisible = ref(false)
const detailActiveTab = ref('basic')
const currentDetail = ref({})

const handleDetail = (row) => {
  currentDetail.value = { ...row }
  detailActiveTab.value = 'basic'
  detailDrawerVisible.value = true
}


// 商品列表搜索和分页条件，对应后端的接收字段
const searchQuery = reactive({
  type: 1,              // 商品状态分类页签（1=销售中, 2=仓库中, 6=回收站等）
  store_name: '',       // 搜索关键字的值
  field_key: 'all',     // 搜索类型下拉框：all(全部), product_id(商品ID), store_name(商品名称)
  cate_id: null,        // 商品分类
  product_type: null,   // 商品类型(0:普通商品，1：卡密，3：虚拟商品等)
  priceMin: '',         // 价格区间下限（前端用，组装给后端为 price_range）
  priceMax: '',         // 价格区间上限
  salesMin: '',         // 销量区间下限（前端用，组装给后端为 sales_range）
  salesMax: '',         // 销量区间上限
  page: 1,              // 当前页码
  limit: 20             // 每页条数
})

const form = reactive({
  id: null,
  storeName: '',
  price: 0,
  stock: 0,
  isShow: 1,
  image: ''
})

// 将前端零散的状态值组装为符合 PHP 接口标准的查询参数格式
const buildParams = () => {
  const { priceMin, priceMax, salesMin, salesMax, ...base } = searchQuery
  return {
    ...base,
    type: Number(searchQuery.type),
    price_range: (priceMin || priceMax) ? `${priceMin || ''}-${priceMax || ''}` : '',
    sales_range: (salesMin || salesMax) ? `${salesMin || ''}-${salesMax || ''}` : ''
  }
}

// 请求获取各状态(Tab页签)的统计数据(销售中、回收站等)
// 传入当前的搜索条件(searchQuery)以保证各个页签的数字在特定搜索场景下依然精确联动
const fetchHeaderStats = async () => {
  try {
    const params = buildParams()
    const res = await axios.get('/api/admin/store/product/status_statistics', { params })
    if (res.data.code === 200) {
      headerStats.value = res.data.data
    }
  } catch (error) {
    console.error('获取顶部统计失败')
  }
}

const handleTabChange = async (val) => {
  searchQuery.type = Number(val)
  searchQuery.page = 1
  await nextTick()
  fetchData()
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = buildParams()
    
    const res = await axios.get('/api/admin/store/product/list', { params })
    if (res.data.code === 200) {
      const records = res.data.data.records || res.data.data
      // 除了出售中的商品(type=1)是上架状态，其他列表的商品在UI上均作为下架状态处理
      if (searchQuery.type !== 1) {
        records.forEach(item => {
          item.isShow = 0
        })
      }
      tableData.value = records
      total.value = res.data.data.total || tableData.value.length
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
  searchQuery.store_name = ''
  searchQuery.field_key = 'all'
  searchQuery.cate_id = null
  searchQuery.product_type = null
  searchQuery.priceMin = ''
  searchQuery.priceMax = ''
  searchQuery.salesMin = ''
  searchQuery.salesMax = ''
  searchQuery.page = 1
  fetchData()
}

const handleAdd = () => {
  dialogTitle.value = '发布商品'
  form.id = null
  form.storeName = ''
  form.price = 0
  form.stock = 0
  form.isShow = 1
  form.image = ''
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑商品'
  form.id = row.id
  form.storeName = row.storeName
  form.price = row.price
  form.stock = row.stock
  form.isShow = row.isShow
  form.image = row.image || ''
  dialogVisible.value = true
}

const handleStatusChange = async (row) => {
  try {
    const res = await axios.post(`/api/admin/store/product/save`, row)
    if (res.data.code === 200) {
      ElMessage.success('商品状态更新成功')
      fetchHeaderStats() // 刷新顶部统计
    } else {
      row.isShow = row.isShow === 1 ? 0 : 1
      ElMessage.error(res.data.msg || '状态修改失败')
    }
  } catch(e) {
    row.isShow = row.isShow === 1 ? 0 : 1
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
      const res = await axios.delete(`/api/admin/store/product/delete/${row.id}`)
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

const handleExport = async () => {
  ElMessage.success('开始导出商品数据...')
}

const submitForm = async () => {
  try {
    const res = await axios.post(`/api/admin/store/product/save`, form)
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

.drawer-header-info {
  display: flex;
  align-items: center;
  background-color: #e6f7ff;
  padding: 15px;
  border-radius: 4px;
}
.detail-section {
  margin-bottom: 20px;
}
.detail-title {
  font-size: 15px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}
.title-bar {
  display: inline-block;
  width: 4px;
  height: 16px;
  background-color: var(--el-color-primary);
  margin-right: 8px;
  border-radius: 2px;
}
.detail-row {
  line-height: 2.5;
}
.detail-item {
  color: #333;
}
.detail-label {
  color: #666;
}
</style>
