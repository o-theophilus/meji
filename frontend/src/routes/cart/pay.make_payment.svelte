<script>
	import { goto } from '$app/navigation';
	import { user, module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Info from '$lib/info.svelte';
	import Email_Admin from './pay.email_template_admin.svelte';
	import Email_User from './pay.email_template_user.svelte';
	let email_template_admin;
	let email_template_user;

	export let cart;
	export let items;
	let error = {};

	const order_check = async () => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/check`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			make_payment(resp.pay);
		} else {
			error = resp;
		}
	};

	const make_payment = async (pay) => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/check`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
		} else {
			error = resp;
		}

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
				email_template_admin: email_template_admin.innerHTML.replace(/&amp;/g, '&'),
				email_template_user: email_template_user.innerHTML.replace(/&amp;/g, '&')
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$user.cart = resp.user.cart;
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

<div class="row">
	<Button primary on:click={order_check}>Make Payment</Button>
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

<div bind:this={email_template_admin} style="display: none;">
	<Email_Admin order={cart} {items} />
</div>
<div bind:this={email_template_user} style="display: none;">
	<Email_User order={cart} {items} />
</div>

<style>
	.row {
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
		font-weight: 700;
	}
	a:hover {
		color: var(--cl1_b);
	}
</style>
