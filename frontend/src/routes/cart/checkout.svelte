<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { user, module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Body from '$lib/comp/card_body_item.svelte';
	import Button from '$lib/comp/button.svelte';

	import Login from '../auth/login.svelte';

	export let total = 0;
	let error;

	const login = async () => {
		$module = {
			module: Login,
			data: {
				message: 'Please login to checkout',
				return_url: $page.url.pathname
			}
		};
	};
	const check_out = async () => {
		if (!$user.login) {
			login();
		} else {
			$loading = true;
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}order`, {
				method: 'post',
				headers: {
					'Content-Type': 'application/json',
					Authorization: $token
				}
			});

			if (_resp.ok) {
				let resp = await _resp.json();

				if (resp.status == 200) {
					$user = resp.data.user;
					goto(`/order/${resp.data.order_key}`);
				} else if (resp.status == 102) {
					login();
				} else {
					error = resp.message;
				}
			}
		}
	};
</script>

<Body>
	<div class="total_amount">
		<div class="total">Total Amount</div>
		<div class="amount">
			₦{total.toLocaleString()}
		</div>
	</div>
	<Button name="Checkout" icon="cart_out" class="primary" on:click={check_out} />
	{#if error}
		{error}
	{/if}
</Body>

<style>
	.total_amount {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.total,
	.amount {
		font-weight: 500;
	}
	.amount {
		font-size: 1.2rem;
		color: var(--color3);
	}
</style>
