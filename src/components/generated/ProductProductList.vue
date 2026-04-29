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
                  <el-option v-for="item in categoryOptions" :key="item.id" :label="item.cateName" :value="item.id" />
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
            <div style="padding: 14px 20px; background-color: #fafafa; border-radius: 4px;">
              <el-row :gutter="20">
                <el-col :span="8">商品分类：{{ getCateNames(props.row.cateId) || '-' }}</el-col>
                <el-col :span="8">商品市场价格：{{ formatMoney(props.row.otPrice) }}</el-col>
                <el-col :span="8">成本价：{{ formatMoney(props.row.cost) }}</el-col>
              </el-row>
              <el-row :gutter="20" style="margin-top: 10px;">
                <el-col :span="8">收藏：{{ toInt(props.row.collect) }}</el-col>
                <el-col :span="8">虚拟销量：{{ toInt(props.row.ficti) }}</el-col>
              </el-row>
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
            <span style="color: #409EFF; margin-right: 4px;">【{{ getSpecTypeName(scope.row.specType) }}】</span>
            <span style="color: #409EFF;">{{ scope.row.storeName }}</span>
          </template>
        </el-table-column>
        <el-table-column label="商品来源" width="100" align="center">
          <template #default="scope">{{ getSourceName(scope.row.type) }}</template>
        </el-table-column>
        <el-table-column label="商品类型" width="100" align="center">
          <template #default="scope">{{ getProductTypeName(scope.row.productType) }}</template>
        </el-table-column>
        <el-table-column prop="price" label="商品售价" width="100" align="center">
          <template #default="scope">
            <span>{{ formatMoney(scope.row.price) }}</span>
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
    <el-drawer :title="currentDetail.id ? '编辑商品' : '发布商品'" v-model="detailDrawerVisible" size="70%">
      <div class="drawer-header-info" v-if="currentDetail.id">
        <el-icon color="var(--el-color-primary)" size="24"><Goods /></el-icon>
        <span style="margin-left: 10px; font-weight: bold;">{{ currentDetail.storeName }}（商品ID：{{ currentDetail.id }}）</span>
      </div>
      <el-form :model="currentDetail" label-width="100px" style="margin-top: 20px;">
        <el-tabs v-model="detailActiveTab">
          <el-tab-pane label="基础信息" name="basic">
            <div class="detail-section">
              <h3 class="detail-title"><span class="title-bar"></span>基础信息</h3>
              <el-row :gutter="20">
                <el-col :span="24">
                  <el-form-item label="商品名称" required>
                    <el-input v-model="currentDetail.storeName" placeholder="请输入商品名称" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="商品分类" required>
                    <el-cascader v-model="currentDetail.cateId" :options="categoryOptions" :props="{ checkStrictly: true, value: 'id', label: 'cateName' }" clearable placeholder="请选择商品分类" style="width: 100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="商品品牌">
                    <el-select v-model="currentDetail.brandId" placeholder="请选择品牌" clearable style="width: 100%">
                      <el-option v-for="b in brandOptions" :key="b.id" :label="b.brandName" :value="b.id" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="商品单位">
                    <el-input v-model="currentDetail.unitName" placeholder="如：件、个" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="商品编码">
                    <el-input v-model="currentDetail.code" placeholder="请输入商品编码" />
                  </el-form-item>
                </el-col>
                <el-col :span="24">
                  <el-form-item label="商品轮播图">
                    <el-input type="textarea" v-model="currentDetail.sliderImage" :rows="2" placeholder="请输入轮播图URL，多个以逗号分隔" />
                    <div style="display: flex; gap: 10px; margin-top: 10px;" v-if="currentDetailImages.length">
                      <el-image v-for="(img, idx) in currentDetailImages" :key="idx" :src="img" style="width: 60px; height: 60px; border-radius: 4px; border: 1px solid #eee;" fit="cover" />
                    </div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-tab-pane>
            
          <el-tab-pane label="物流设置" name="logistics">
            <el-form-item label="配送方式" required>
              <el-checkbox-group v-model="deliveryTypeArr">
                <el-checkbox label="1">快递</el-checkbox>
                <el-checkbox label="2">自提</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="运费设置" required>
              <el-radio-group v-model="currentDetail.freight">
                <el-radio :label="3">包邮</el-radio>
                <el-radio :label="1">固定邮费</el-radio>
                <el-radio :label="2">运费模板</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="邮费" v-if="currentDetail.freight === 1">
              <el-input-number v-model="currentDetail.postage" :precision="2" :min="0" :controls="false" style="width: 200px" />
            </el-form-item>
            <el-form-item label="运费模板" v-if="currentDetail.freight === 2">
              <el-select v-model="currentDetail.tempId" placeholder="请选择运费模板" style="width: 200px">
                <!-- 预留运费模板下拉数据选项 -->
                <el-option label="默认模板" :value="1" />
              </el-select>
            </el-form-item>
          </el-tab-pane>
          
          <el-tab-pane label="规格库存" name="spec">
            <el-table :data="specTableData" v-loading="specLoading" border style="width: 100%;">
              <el-table-column prop="sku" label="规格名称" min-width="120" />
              <el-table-column label="图片" width="100" align="center">
                <template #default="scope">
                  <el-input v-model="scope.row.image" placeholder="URL" size="small" />
                </template>
              </el-table-column>
              <el-table-column label="售价" width="110" align="center">
                <template #default="scope">
                  <el-input-number v-model="scope.row.price" :precision="2" :controls="false" size="small" style="width: 100%" />
                </template>
              </el-table-column>
              <el-table-column label="成本价" width="110" align="center">
                <template #default="scope">
                  <el-input-number v-model="scope.row.cost" :precision="2" :controls="false" size="small" style="width: 100%" />
                </template>
              </el-table-column>
              <el-table-column label="结算价" width="110" align="center">
                <template #default="scope">
                  <el-input-number v-model="scope.row.settlePrice" :precision="2" :controls="false" size="small" style="width: 100%" />
                </template>
              </el-table-column>
              <el-table-column label="划线价" width="110" align="center">
                <template #default="scope">
                  <el-input-number v-model="scope.row.otPrice" :precision="2" :controls="false" size="small" style="width: 100%" />
                </template>
              </el-table-column>
              <el-table-column label="库存" width="110" align="center">
                <template #default="scope">
                  <el-input-number v-model="scope.row.stock" :min="0" :controls="false" size="small" style="width: 100%" />
                </template>
              </el-table-column>
              <el-table-column label="商品编码" width="120" align="center">
                <template #default="scope">
                  <el-input v-model="scope.row.sku" size="small" />
                </template>
              </el-table-column>
              <el-table-column label="重量(KG)" width="100" align="center">
                <template #default="scope">
                  <el-input-number v-model="scope.row.weight" :precision="2" :controls="false" size="small" style="width: 100%" />
                </template>
              </el-table-column>
            </el-table>
            <div style="margin-top: 16px; display: flex; justify-content: flex-end;">
              <el-pagination
                background
                layout="total, sizes, prev, pager, next, jumper"
                :total="specTotal"
                :page-sizes="[10, 20, 50, 100]"
                v-model:current-page="specPage"
                v-model:page-size="specLimit"
                @current-change="fetchSpecList"
                @size-change="fetchSpecList"
              />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="商品详情" name="content">
            <el-form-item label="图文详情" label-width="80px">
              <el-input type="textarea" v-model="currentDetail.description" :rows="15" placeholder="请输入商品图文详情 (支持HTML代码)" />
            </el-form-item>
          </el-tab-pane>
          
          <el-tab-pane label="佣金/会员价" name="commission">
            <el-form-item label="是否参与">
              <el-radio-group v-model="currentDetail.isBrokerage">
                <el-radio :label="0">不参与返佣</el-radio>
                <el-radio :label="1">参与返佣</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="返佣设置" v-if="currentDetail.isBrokerage === 1">
              <el-radio-group v-model="currentDetail.brokerageType">
                <el-radio :label="1">默认比例</el-radio>
                <el-radio :label="2">自定义佣金</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="付费会员">
              <el-switch v-model="currentDetail.isVipProduct" :active-value="1" :inactive-value="0" />
            </el-form-item>
            <el-form-item label="等级会员">
              <el-radio-group v-model="currentDetail.levelType">
                <el-radio :label="1">默认价格</el-radio>
                <el-radio :label="2">自定义</el-radio>
              </el-radio-group>
            </el-form-item>
            <!-- 预留返佣/会员价格表格位置，此处简单展示一个占位表格 -->
            <el-table :data="specTableData" v-if="currentDetail.isBrokerage === 1 || currentDetail.levelType === 2" border style="width: 100%; margin-top: 15px;">
              <el-table-column prop="sku" label="产品规格" min-width="120" />
              <el-table-column prop="price" label="售价" width="100" align="center" />
              <el-table-column label="一级返佣" width="100" align="center" v-if="currentDetail.isBrokerage === 1 && currentDetail.brokerageType === 2">
                <template #default>3%</template>
              </el-table-column>
              <el-table-column label="二级返佣" width="100" align="center" v-if="currentDetail.isBrokerage === 1 && currentDetail.brokerageType === 2">
                <template #default>2%</template>
              </el-table-column>
              <el-table-column label="青铜会员" width="100" align="center" v-if="currentDetail.levelType === 2">
                <template #default>100%</template>
              </el-table-column>
              <el-table-column label="白银会员" width="100" align="center" v-if="currentDetail.levelType === 2">
                <template #default>95%</template>
              </el-table-column>
            </el-table>
          </el-tab-pane>

          <el-tab-pane label="营销设置" name="marketing">
            <el-form-item label="服务保障">
              <el-checkbox-group v-model="ensureIdArr">
                <el-checkbox label="1">7天无理由退货</el-checkbox>
                <el-checkbox label="2">退换货运费险</el-checkbox>
                <el-checkbox label="3">店铺发货&售后</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="起购数量">
              <el-input-number v-model="currentDetail.minQty" :min="0" :controls="false" style="width: 200px" />
              <span style="margin-left: 10px; color: #999;">件/人</span>
            </el-form-item>
            <el-form-item label="是否限购">
              <el-switch v-model="currentDetail.isLimit" :active-value="1" :inactive-value="0" />
            </el-form-item>
            <div v-if="currentDetail.isLimit === 1" style="background: #f8f8f8; padding: 15px; margin-bottom: 15px;">
              <el-form-item label="限购类型">
                <el-radio-group v-model="currentDetail.limitType">
                  <el-radio :label="1">单次限购</el-radio>
                  <el-radio :label="2">永久限购</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="限购数量">
                <el-input-number v-model="currentDetail.limitNum" :min="0" :controls="false" style="width: 200px" />
              </el-form-item>
            </div>
            <el-form-item label="预售商品">
              <el-switch v-model="currentDetail.isPresaleProduct" :active-value="1" :inactive-value="0" />
            </el-form-item>
            <el-form-item label="优品推荐">
              <el-switch v-model="currentDetail.isGood" :active-value="1" :inactive-value="0" />
            </el-form-item>
            <el-form-item label="支持送礼">
              <el-switch v-model="currentDetail.isSendGift" :active-value="1" :inactive-value="0" />
            </el-form-item>
          </el-tab-pane>

          <el-tab-pane label="其他设置" name="other">
            <el-form-item label="商品关键字">
              <el-input v-model="currentDetail.keyword" placeholder="多个关键字用逗号分隔" />
            </el-form-item>
            <el-form-item label="商品简介">
              <el-input type="textarea" v-model="currentDetail.storeInfo" :rows="3" placeholder="请输入商品简介" />
            </el-form-item>
            <el-form-item label="分销文案">
              <el-input type="textarea" v-model="currentDetail.shareContent" :rows="3" placeholder="请输入分销文案" />
            </el-form-item>
            <el-form-item label="商品口令">
              <el-input v-model="currentDetail.commandWord" placeholder="请输入商品口令" />
            </el-form-item>
            <el-form-item label="商品推荐图">
              <el-input type="textarea" v-model="currentDetail.recommendImage" :rows="2" placeholder="请输入推荐图URL" />
              <div style="margin-top: 10px;" v-if="currentDetail.recommendImage">
                <el-image :src="currentDetail.recommendImage" style="width: 100px; height: 40px; border-radius: 4px;" fit="cover" />
              </div>
            </el-form-item>
            <el-form-item label="商品参数">
              <el-button type="primary" size="small" plain style="margin-bottom: 10px;">添加参数</el-button>
              <el-table :data="[]" border style="width: 100%;">
                <el-table-column label="参数名称" width="150"></el-table-column>
                <el-table-column label="参数值"></el-table-column>
                <el-table-column label="操作" width="80" align="center"></el-table-column>
              </el-table>
            </el-form-item>
            <el-form-item label="自定义留言">
              <el-switch v-model="currentDetail.customFormOpen" />
            </el-form-item>
            
            <!-- 原有的排序等独立为块或融入 -->
            <div class="detail-section" style="margin-top: 20px;">
              <h3 class="detail-title"><span class="title-bar"></span>统计排序</h3>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="已售数量">
                    <el-input-number v-model="currentDetail.sales" :min="0" style="width: 100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="虚拟销量">
                    <el-input-number v-model="currentDetail.ficti" :min="0" style="width: 100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="排序">
                    <el-input-number v-model="currentDetail.sort" :min="0" style="width: 100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="赠送积分">
                    <el-input-number v-model="currentDetail.giveIntegral" :min="0" style="width: 100%" />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="商品评论" name="reply">
            <el-table :data="replyTableData" v-loading="replyLoading" border style="width: 100%;">
              <el-table-column prop="id" label="评论ID" width="90" align="center" />
              <el-table-column label="商品信息" min-width="160">
                <template #default>{{ currentDetail.storeName }}</template>
              </el-table-column>
              <el-table-column label="评价内容" min-width="260">
                <template #default="scope">
                  <div>用户：{{ scope.row.nickname || scope.row.uid }}</div>
                  <div>评分：{{ toInt(scope.row.productScore) }}</div>
                  <div>{{ scope.row.comment || '-' }}</div>
                </template>
              </el-table-column>
              <el-table-column label="评价时间" width="170" align="center">
                <template #default="scope">{{ formatTime(scope.row.addTime) }}</template>
              </el-table-column>
              <el-table-column label="操作" width="180" align="center">
                <template #default="scope">
                  <el-button size="small" type="primary" link @click="openReply(scope.row)">回复</el-button>
                  <el-button size="small" type="danger" link @click="deleteReply(scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div style="margin-top: 16px; display: flex; justify-content: flex-end;">
              <el-pagination
                background
                layout="total, sizes, prev, pager, next, jumper"
                :total="replyTotal"
                :page-sizes="[10, 20, 50, 100]"
                v-model:current-page="replyPage"
                v-model:page-size="replyLimit"
                @current-change="fetchReplyList"
                @size-change="fetchReplyList"
              />
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-form>
      <template #footer>
        <div style="text-align: right; padding-top: 10px;">
          <el-button @click="detailDrawerVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveProduct">保存设置</el-button>
        </div>
      </template>
    </el-drawer>

    <el-dialog title="回复评论" v-model="replyDialogVisible" width="520px">
      <el-form label-width="90px">
        <el-form-item label="回复内容">
          <el-input type="textarea" v-model="replyContent" :rows="4" placeholder="请输入回复内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="replyDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReply">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>


<script setup>
import { ref, reactive, onMounted, inject, nextTick, computed } from 'vue'
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

const detailDrawerVisible = ref(false)
const detailActiveTab = ref('basic')
const currentDetail = ref({})

const selectedCount = ref(0)
const handleSelectionChange = (val) => {
  selectedCount.value = val.length
}

const categoryOptions = ref([])
const categoryNameMap = ref({})
const brandNameMap = ref({})
const brandOptions = ref([])

const toInt = (v) => {
  const n = Number(v)
  return Number.isFinite(n) ? Math.trunc(n) : 0
}

const formatMoney = (v) => {
  const n = Number(v)
  if (!Number.isFinite(n)) return '0.00'
  return n.toFixed(2)
}

const getSourceName = (v) => {
  const t = Number(v)
  if (t === 1) return '门店'
  if (t === 2) return '供应商'
  return '平台'
}

const getProductTypeName = (v) => {
  const t = Number(v)
  if (t === 1) return '卡密商品'
  if (t === 2) return '优惠券'
  if (t === 3) return '虚拟商品'
  if (t === 4) return '次卡商品'
  return '普通商品'
}

const getSpecTypeName = (v) => {
  const t = Number(v)
  return t === 1 ? '多规格' : '单规格'
}

const getCateNames = (cateIdStr) => {
  if (!cateIdStr) return ''
  const raw = String(cateIdStr).trim()
  if (!raw) return ''
  const ids = raw.split(',').map(s => s.trim()).filter(Boolean)
  const names = ids.map(id => categoryNameMap.value[id]).filter(Boolean)
  return names.join(',')
}

const getBrandName = (brandId) => {
  if (!brandId && brandId !== 0) return '-'
  return brandNameMap.value[String(brandId)] || '-'
}

const formatTime = (ts) => {
  const n = Number(ts)
  if (!Number.isFinite(n) || n <= 0) return '-'
  const d = new Date(n * 1000)
  const pad = (v) => String(v).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

const parseImages = (sliderImage, image) => {
  const list = []
  if (sliderImage) {
    const raw = String(sliderImage).trim()
    if (raw.startsWith('[')) {
      try {
        const arr = JSON.parse(raw)
        if (Array.isArray(arr)) {
          arr.forEach(it => {
            if (it) list.push(String(it))
          })
        }
      } catch (e) {}
    } else {
      raw.split(',').map(s => s.trim()).filter(Boolean).forEach(it => list.push(it))
    }
  }
  if (!list.length && image) list.push(image)
  return list
}

const currentDetailImages = computed(() => parseImages(currentDetail.value.sliderImage, currentDetail.value.image))

const specTableData = ref([])
const specLoading = ref(false)
const specTotal = ref(0)
const specPage = ref(1)
const specLimit = ref(10)

const replyTableData = ref([])
const replyLoading = ref(false)
const replyTotal = ref(0)
const replyPage = ref(1)
const replyLimit = ref(10)

const replyDialogVisible = ref(false)
const replyContent = ref('')
const currentReplyRow = ref(null)

const fetchCategories = async () => {
  const res = await axios.get('/api/admin/store/productCategory/list', { params: { isShow: 1 } })
  if (res.data && res.data.code === 200) {
    categoryOptions.value = res.data.data || []
    const map = {}
    categoryOptions.value.forEach(item => {
      if (item && item.id != null) {
        map[String(item.id)] = item.cateName
      }
    })
    categoryNameMap.value = map
  }
}

const fetchProductInfo = async (id) => {
  const res = await axios.get(`/api/admin/store/product/info/${id}`)
  if (res.data && res.data.code === 200) {
    currentDetail.value = res.data.data || {}
    if (currentDetail.value.deliveryType) {
      deliveryTypeArr.value = currentDetail.value.deliveryType.split(',').filter(v => v)
    } else {
      deliveryTypeArr.value = []
    }
    if (currentDetail.value.ensureId) {
      ensureIdArr.value = currentDetail.value.ensureId.split(',').filter(v => v)
    } else {
      ensureIdArr.value = []
    }
  }
}

const fetchSpecList = async () => {
  if (!currentDetail.value || !currentDetail.value.id) return
  specLoading.value = true
  try {
    const res = await axios.get('/api/admin/store/product/attr_value/list', {
      params: { product_id: currentDetail.value.id, page: specPage.value, limit: specLimit.value }
    })
    if (res.data && res.data.code === 200 && res.data.data) {
      specTableData.value = res.data.data.records || []
      specTotal.value = res.data.data.total || specTableData.value.length
    } else {
      specTableData.value = []
      specTotal.value = 0
    }
  } catch (e) {
    specTableData.value = []
    specTotal.value = 0
  } finally {
    specLoading.value = false
  }
}

const fetchReplyList = async () => {
  if (!currentDetail.value || !currentDetail.value.id) return
  replyLoading.value = true
  try {
    const res = await axios.get('/api/admin/store/product/reply/list', {
      params: { product_id: currentDetail.value.id, page: replyPage.value, limit: replyLimit.value }
    })
    if (res.data && res.data.code === 200 && res.data.data) {
      replyTableData.value = res.data.data.records || []
      replyTotal.value = res.data.data.total || replyTableData.value.length
    } else {
      replyTableData.value = []
      replyTotal.value = 0
    }
  } catch (e) {
    replyTableData.value = []
    replyTotal.value = 0
  } finally {
    replyLoading.value = false
  }
}

const openReply = (row) => {
  currentReplyRow.value = row
  replyContent.value = row.merchantReplyContent || ''
  replyDialogVisible.value = true
}

const submitReply = async () => {
  if (!currentReplyRow.value) return
  try {
    const payload = { id: currentReplyRow.value.id, merchantReplyContent: replyContent.value }
    const res = await axios.post('/api/admin/store/product/reply/set_reply', payload)
    if (res.data && res.data.code === 200) {
      ElMessage.success(res.data.msg || '回复成功')
      replyDialogVisible.value = false
      fetchReplyList()
    } else {
      ElMessage.error(res.data.msg || '回复失败')
    }
  } catch (e) {
    ElMessage.error('网络错误')
  }
}

const deleteReply = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该评论？', '提示', { type: 'warning' })
    const res = await axios.post('/api/admin/store/product/reply/delete', { id: row.id })
    if (res.data && res.data.code === 200) {
      ElMessage.success(res.data.msg || '删除成功')
      fetchReplyList()
    } else {
      ElMessage.error(res.data.msg || '删除失败')
    }
  } catch (e) {}
}

const fetchBrands = async () => {
  const res = await axios.get('/api/admin/store/product/brand/list', { params: { page: 1, limit: 1000 } })
  if (res.data && res.data.code === 200 && res.data.data && Array.isArray(res.data.data.records)) {
    brandOptions.value = res.data.data.records
    const map = {}
    res.data.data.records.forEach(item => {
      if (item && item.id != null) {
        map[String(item.id)] = item.brandName
      }
    })
    brandNameMap.value = map
  }
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

const handleAdd = () => {
  currentDetail.value = {
    id: null,
    storeName: '',
    cateId: null,
    brandId: null,
    unitName: '',
    code: '',
    sliderImage: '',
    deliveryType: '',
    ensureId: '',
    freight: 1,
    sales: 0,
    ficti: 0,
    sort: 0,
    giveIntegral: 0,
    description: '',
    image: '',
    price: 0,
    stock: 0,
    isShow: 1
  }
  deliveryTypeArr.value = []
  ensureIdArr.value = []
  specTableData.value = []
  replyTableData.value = []
  detailActiveTab.value = 'basic'
  detailDrawerVisible.value = true
}

const handleEdit = (row) => {
  currentDetail.value = { ...row }
  detailActiveTab.value = 'basic'
  detailDrawerVisible.value = true
  specPage.value = 1
  replyPage.value = 1
  fetchProductInfo(row.id).then(() => {
    fetchSpecList()
    fetchReplyList()
  })
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

const deliveryTypeArr = ref([])
const ensureIdArr = ref([])

const handleSaveProduct = async () => {
  try {
    const isEdit = !!currentDetail.value.id
    
    // Convert arrays back to comma separated strings
    currentDetail.value.deliveryType = deliveryTypeArr.value.join(',')
    currentDetail.value.ensureId = ensureIdArr.value.join(',')
    
    // 1. 保存主商品信息
    const productRes = await axios.post('/api/admin/store/product/save', currentDetail.value)
    if (productRes.data.code !== 200) {
      return ElMessage.error(productRes.data.msg || '保存商品信息失败')
    }
    
    const productId = isEdit ? currentDetail.value.id : productRes.data.data
    
    // 2. 保存图文详情
    if (currentDetail.value.description !== undefined) {
      await axios.post('/api/admin/store/product/description/save', {
        productId,
        description: currentDetail.value.description,
        type: 0
      })
    }
    
    // 3. 保存规格库存 (若有修改)
    if (specTableData.value && specTableData.value.length > 0) {
      const specPayload = specTableData.value.map(item => ({
        ...item,
        productId
      }))
      await axios.post('/api/admin/store/product/attr_value/save', specPayload)
    }
    
    ElMessage.success(isEdit ? '商品编辑成功' : '商品发布成功')
    detailDrawerVisible.value = false
    fetchData()
    fetchHeaderStats()
  } catch (error) {
    console.error('保存商品失败', error)
    ElMessage.error('保存失败，请检查网络')
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



onMounted(() => {
  fetchCategories()
  fetchBrands()
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
