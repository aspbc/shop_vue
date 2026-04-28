<template>
  <div class="product-list-container">
    <el-card shadow="never" class="table-card">
      <!-- 1. 商品状态多页签 -->
      <el-tabs v-model="searchQuery.tabStatus" @tab-click="handleTabClick" class="status-tabs">
        <el-tab-pane name="selling">
          <template #label>销售中 ({{ headerStats.selling || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane name="warehouse">
          <template #label>仓库中 ({{ headerStats.warehouse || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane name="soldOut">
          <template #label>已售罄 ({{ headerStats.soldOut || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane name="alert">
          <template #label>库存预警 ({{ headerStats.alert || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane name="recycle">
          <template #label>回收站 ({{ headerStats.recycle || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane name="pending">
          <template #label>待审核 ({{ headerStats.pending || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane name="rejected">
          <template #label>审核未通过 ({{ headerStats.rejected || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane name="forced">
          <template #label>强制下架 ({{ headerStats.forced || 0 }})</template>
        </el-tab-pane>
      </el-tabs>

      <!-- 2. 多维搜索参数区域 -->
      <div class="search-wrapper">
        <el-form :inline="true" :model="searchQuery" class="advanced-search-form" size="default">
          <el-row :gutter="15">
            <el-col :span="6">
              <el-form-item label="商品搜索" style="width: 100%;">
                <el-input v-model="searchQuery.keyword" placeholder="商品名称/关键字/ID" clearable />
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="商品分类" style="width: 100%;">
                <el-select v-model="searchQuery.cateId" placeholder="全部分类" clearable style="width: 100%;">
                  <el-option label="手机数码" value="1" />
                  <el-option label="家用电器" value="2" />
                  <el-option label="服装服饰" value="3" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="商品类型" style="width: 100%;">
                <el-select v-model="searchQuery.type" placeholder="全部" clearable style="width: 100%;">
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
          <el-button type="warning" plain v-if="searchQuery.tabStatus === 'warehouse'">批量上架</el-button>
          <el-button type="warning" plain v-if="searchQuery.tabStatus === 'selling'">批量下架</el-button>
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
        <el-table-column label="状态" width="100" align="center" v-if="searchQuery.tabStatus !== 'recycle'">
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
            <el-button size="small" type="primary" link @click="handleEdit(scope.row)" v-if="searchQuery.tabStatus !== 'recycle'">编辑</el-button>
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

const handleDetail = (row) => {
  ElMessage.info('查看商品详情: ' + row.id)
}

const handleStock = (row) => {
  ElMessage.info('管理商品库存: ' + row.id)
}

const searchQuery = reactive({
  tabStatus: 'selling',
  keyword: '',
  cateId: null,
  type: null,
  priceMin: '',
  priceMax: '',
  salesMin: '',
  salesMax: '',
  isShow: null, // 将根据 tabStatus 自动计算
  page: 1,
  limit: 20
})

const form = reactive({
  id: null,
  storeName: '',
  price: 0,
  stock: 0,
  isShow: 1,
  image: ''
})

const fetchHeaderStats = async () => {
  try {
    const res = await axios.get('/api/admin/store/product/headerStats')
    if (res.data.code === 200) {
      headerStats.value = res.data.data
    }
  } catch (error) {
    console.error('获取顶部统计失败')
  }
}

const handleTabClick = (tab) => {
  searchQuery.page = 1
  fetchData()
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = { ...searchQuery }
    // 根据 Tab 状态转换查询条件
    if (params.tabStatus === 'selling') params.isShow = 1
    else if (params.tabStatus === 'warehouse') params.isShow = 0
    else params.isShow = null
    
    const res = await axios.get('/api/admin/store/product/list', { params })
    if (res.data.code === 200) {
      tableData.value = res.data.data.records || res.data.data
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
  searchQuery.keyword = ''
  searchQuery.cateId = null
  searchQuery.type = null
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
</style>
