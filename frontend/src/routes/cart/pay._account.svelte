<script>
	import { user, module, portal, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import Button from '$lib/button.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';

	let cart = { ...$module.cart };
	let error = {};
	let amount = cart.transaction.account;

	const validate = async () => {
		error = {};

		if (!Number(amount) && amount != 0) {
			error.amount = 'invalid amount';
		} else if (amount > $user.acc_balance) {
			error.amount = `amount larger than available balance (₦${$user.acc_balance.toLocaleString()})`;
		} else if (amount > pay) {
			error.amount = `amount larger than total cost (₦${pay.toLocaleString()})`;
		} else if (amount < 0) {
			error.amount = 'negative amount not allowed';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart_account`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ amount })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'account',
				data: resp.cart.transaction.account
			};
			$module = '';
			$toast = {
				status: '200',
				message: 'Amount changed'
			};
		} else {
			error = resp;
		}
	};

	let pay = cart.transaction.total_items + cart.transaction.delivery_fee - cart.transaction.account;
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Account</b>
		Enter amount to deduct from your account
	</svelte:fragment>

	<IG
		name="amount"
		label="Amount (₦)"
		{error}
		bind:value={amount}
		type="number"
		placeholder="Amount here"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" on:click={validate}>Ok</Button>
</Form>

<style>
</style>
