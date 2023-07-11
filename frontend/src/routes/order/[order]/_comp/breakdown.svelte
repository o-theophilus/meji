<script>
	import { currency, module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import HR from '$lib/comp/hr.svelte';
	import Item from './breakdown_item.svelte';
	import Voucher from '../_voucher.svelte';
	import Total from './breakdown_total.svelte';
	import Account from '../_account.svelte';

	export let order;
	export let user;

	let voucher_form = () => {
		$module = {
			module: Voucher
		};
	};

	let total_items = order.info.total_items + order.info.delivery_fee;
</script>

<Card>
	<Title title="Cost Breakdown" />
	<Body>
		<Item items={order.items} />
		<br />
		<Total title={'Delivery Fee'} value={order.info.delivery_fee} />
		<HR />
		<Total
			title={'Total Cost'}
			u_title={user.acc_balance <= 0}
			value={total_items}
			on:title={() => {
				voucher_form();
			}}
		/>
		{#if user.acc_balance > 0}
			<Total
				title={`Acc. Bal (${currency(user.acc_balance)})`}
				value={order.info.account}
				u_title
				u_value
				on:title={() => {
					voucher_form();
				}}
				on:value={() => {
					$module = {
						module: Account,
						data: { order }
					};
				}}
			/>
		{/if}

		<HR />
		<Total title="Pay" value={total_items - order.info.account} />
	</Body>
</Card>

<style>
</style>
