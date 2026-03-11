<script>
	import { Content } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';
	import Card from './card.svelte';
</script>

<Log entity_type={'page'} />
<Meta title="Admin Dashboard" />

<Content>
	<div class="page_title">Admin Dashboard</div>
	<Card title="Sales Today"></Card>
	<Card title="Orders Today"></Card>
	<Card title="New Users Today"></Card>

	<br />
	<Card title="Conversion Rate"></Card>
	<Card title="Revenue Today">
		$4,520
		<br />
		↑ 12% from yesterday
	</Card>
	<br />
	<Card title="SALES CHART">
		Display: line | bar chart
		<br />
		Filter: (Today , 7 days, 30 days, 12 months)
	</Card>
	<Card title="ORDERS STATUS">
		Display: Columns
		<br />
		<br />
		Pending: 12
		<br />
		Processing: 8
		<br />
		Shipped: 24
		<br />
		Returns: 2
	</Card>
	<Card title="TOP PRODUCTS">
		Display: Columns
		<br />
		filter: Most sold products | Highest revenue products
		<br />
		<br />
		Product | Units Sold | Revenue
		<br />
		Product A | 120 sold
	</Card>
	<Card title="TOP Customers">
		Display: Columns
		<br />
		filter: spending | quantity
		<br />
		<br />
		Product | Units Sold | Revenue
		<br />
		Product A | 120 sold
	</Card>
	<Card title="RECENT ORDERS">
		Display: Columns
		<br />
		<br />
		Order ID | Customer | Total | Status
		<br />
		#ORD-1024 | $120 | Paid
	</Card>
	<Card title="ACTIVITY FEED">
		Display: Columns
		<br />
		<br />
		New order placed | time
		<br />
		Product updated | time
		<br />
		Customer registered | time
	</Card>
	<Card title="Low Stock">
		Display: Columns
		<br />
		<br />
		Black Hoodie | (3 left)
		<br />
		Nike Air Max | (3 left)
	</Card>
	<Card title="Cart analytics">
		Display: Columns
		<br />
		<br />
		Abandoned | 3
		<br />
		Checkout | 3
	</Card>
	<Card title="Coupon Usage">
		Display: Columns
		<br />
		<br />
		Count | 3
		<br />
		Value | 3
	</Card>
	<Card title="Traffic / Analytics">
		Display: Columns
		<br />
		<br />
		page | 3
	</Card>
</Content>

<style>
</style>
