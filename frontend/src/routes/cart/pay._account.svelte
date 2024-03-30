<script>
	import { user, module, portal, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import Button from '$lib/button.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';

	let cart = { ...$module.cart };
	let pay = cart.cost_items + cart.cost_delivery - cart.pay_account;
	let error = {};
	let amount = cart.pay_account;

	const validate = async () => {
		error = {};

		if (!Number(amount) && amount != 0) {
			error.amount = 'invalid amount';
		} else if (amount > $user.account_balance) {
			error.amount = `amount larger than available balance (₦${$user.account_balance.toLocaleString()})`;
		} else if (amount > pay) {
			error.amount = `amount larger than total cost (₦${pay.toLocaleString()})`;
		} else if (amount < 0) {
			error.amount = 'negative amount not allowed';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/account`, {
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
				type: 'pay_account',
				data: resp.cart
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
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Account</b>
		Enter amount to deduct from your account
	</svelte:fragment>

	Acc. Bal: ₦{$user.account_balance.toLocaleString()}

	<br />

	<br />
	<IG
		name="amount"
		label="Amount (₦)"
		{error}
		bind:value={amount}
		type="number"
		placeholder="Amount here"
	/>

	Remaining: ₦{($user.account_balance - amount).toLocaleString()}

	<br />
	<br />

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
