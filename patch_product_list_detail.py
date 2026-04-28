import re

file_path = "/workspace/shop_vue/src/components/generated/ProductProductList.vue"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Stock Dialog and Detail Drawer to template (just before closing </div> of product-list-container)
dialogs_html = """
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
"""

content = content.replace("  </div>\n</template>", dialogs_html)

# 2. Add imports for Goods icon
content = content.replace("import { Search, ArrowDown, ArrowUp } from '@element-plus/icons-vue'", "import { Search, ArrowDown, ArrowUp, Goods } from '@element-plus/icons-vue'")

# 3. Add JS state and methods for Stock and Detail
old_js = """const handleDetail = (row) => {
  ElMessage.info('查看商品详情: ' + row.id)
}

const handleStock = (row) => {
  ElMessage.info('管理商品库存: ' + row.id)
}"""

new_js = """
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

const handleStock = (row) => {
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
}

const detailDrawerVisible = ref(false)
const detailActiveTab = ref('basic')
const currentDetail = ref({})

const handleDetail = (row) => {
  currentDetail.value = { ...row }
  detailActiveTab.value = 'basic'
  detailDrawerVisible.value = true
}
"""

content = content.replace(old_js, new_js)

# 4. Add CSS styles
styles = """
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
"""

content = content.replace("</style>", styles)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
