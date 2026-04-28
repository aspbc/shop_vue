import re

file_path = "/workspace/shop_vue/src/components/generated/ProductProductList.vue"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Tabs
old_tabs = """      <el-tabs v-model="searchQuery.tabStatus" @tab-click="handleTabClick" class="status-tabs">
        <el-tab-pane name="selling">
          <template #label>出售中 ({{ headerStats.selling || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane name="warehouse">
          <template #label>仓库中 ({{ headerStats.warehouse || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane name="soldOut">
          <template #label>已售罄 ({{ headerStats.soldOut || 0 }})</template>
        </el-tab-pane>
        <el-tab-pane name="recycle">
          <template #label>回收站 ({{ headerStats.recycle || 0 }})</template>
        </el-tab-pane>
      </el-tabs>"""

new_tabs = """      <el-tabs v-model="searchQuery.tabStatus" @tab-click="handleTabClick" class="status-tabs">
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
      </el-tabs>"""

content = content.replace(old_tabs, new_tabs)

# 2. Update Table columns
old_table_start = """      <el-table :data="tableData" style="width: 100%" v-loading="loading" border>
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
        <el-table-column prop="storeName" label="商品名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="price" label="商品售价" width="100" align="center">
          <template #default="scope">
            <span style="color: #f5222d; font-weight: bold;">¥{{ scope.row.price || '0.00' }}</span>
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
        <el-table-column label="操作" width="220" fixed="right" align="center">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleEdit(scope.row)" v-if="searchQuery.tabStatus !== 'recycle'">编辑</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(scope.row)" v-if="searchQuery.tabStatus !== 'recycle'">移入回收站</el-button>
            <el-button size="small" type="success" link v-if="searchQuery.tabStatus === 'recycle'">恢复商品</el-button>
          </template>
        </el-table-column>
      </el-table>"""

new_table_start = """      <el-table :data="tableData" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
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
      </el-table>"""

content = content.replace(old_table_start, new_table_start)

# 3. Add selectedCount and handleSelectionChange
old_script_stats = """const headerStats = ref({
  selling: 0,
  warehouse: 0,
  soldOut: 0,
  recycle: 0
})"""

new_script_stats = """const headerStats = ref({
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
}"""

content = content.replace(old_script_stats, new_script_stats)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
