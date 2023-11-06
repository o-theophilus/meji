<script>
	import { goto } from '$app/navigation';
	import { user, module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';
	import Email from './pay.email_template.svelte';
	let email_template;

	export let cart;
	export let pay;
	let error = {};

	const make_payment = async () => {
		if (pay > 0) {
			const paystack = PaystackPop.setup({
				key: import.meta.env.VITE_PAYSTACK_KEY,
				email: $user.email,
				amount: pay * 100,
				callback: (resp) => {
					submit(resp.reference);
				},
				onCancel: () => {
					$module = {
						module: Info,
						status: 400,
						title: 'Payment Canceled',
						message: `The payment process was canceled`,
						button: [
							{
								name: 'Ok',
								icon: 'ok',
								fn: () => {
									$module = '';
								}
							}
						]
					};
				}
			});
			paystack.openIframe();
		} else {
			submit();
		}
	};

	const submit = async (reference = '') => {
		error = {};

		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				reference,
				email_template: email_template.innerHTML.replace(/&amp;/g, '&')
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$user = resp.user;
			goto(`/orders/${resp.order.key}`);

			$module = {
				module: Info,
				status: 200,
				title: 'Successful',
				message: `Your order was placed successfully`,
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};
</script>

<svelte:head>
	<script src="https://js.paystack.co/v2/inline.js"></script>
</svelte:head>

<div class="horizontal">
	<Button class="primary" on:click={make_payment}>Place Order</Button>
</div>
<br />
{#if error.error}
	<p class="error">
		{error.error}
	</p>
	<br />
{/if}

<p class="terms">
	by clicking the order button, you have accepred our
	<a href="/terms">terms and conditions</a>
</p>

<div bind:this={email_template} style="display: none;">
	<Email order={cart} />
</div>

<style>
	.horizontal {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.terms {
		font-size: small;
	}
	a {
		color: var(--cl1);
		text-decoration: none;
		font-weight: 500;
	}
	a:hover {
		color: var(--cl2);
	}
</style>
