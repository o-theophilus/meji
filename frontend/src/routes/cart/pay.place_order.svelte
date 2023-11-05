<script>
	import { user, module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';
	import Email from './pay.email_template.svelte';
	let email_template;

	export let cart;
	let error = {};

	$: {
		cart;
		error = {};
	}

	let pay = 0;

	$: {
		let total_items = 0;
		for (const x in cart.items) {
			total_items += cart.items[x].quantity * cart.items[x].price;
		}

		pay = total_items + cart.transaction.delivery_fee - cart.transaction.account;
	}

	$: complete_address =
		cart.recipient.name &&
		cart.recipient.phone &&
		cart.recipient.address.line &&
		cart.recipient.address.state &&
		cart.recipient.address.country &&
		cart.recipient.address.local_area &&
		cart.recipient.address.postal_code;

	const validate = () => {
		error = {};
		if (!complete_address) {
			error.error = "kindly fill the receiver's information form";
		}

		Object.keys(error).length === 0 && make_payment();
	};

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

		$loading = "loading . . .";
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/${cart.key}`, {
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
			$user.acc_balance = resp.user.acc_balance;
			$portal = {
				type: 'order',
				data: resp.order
			};

			$module = {
				module: Info,
				status: 200,
				title: 'Successful',
				message: `Your order was placed succcessfully`,
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
	<Button class={complete_address ? 'primary' : ''} on:click={validate}>
		Place Order {pay > 0 ? `(Pay ₦${pay.toLocaleString()})` : ''}
	</Button>
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
