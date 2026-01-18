<script>
	import { goto } from '$app/navigation';
	import { app, loading, scroll, module } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';
	import { Dialogue, Note } from '$lib/info';

	import Email_Admin from '../orders/[slug]/email/create_admin.svelte';
	import Email_User from '../orders/[slug]/email/create_user.svelte';
	let email_template_admin;
	let email_template_user;

	let { ops = $bindable() } = $props();

	const make_payment = async () => {
		ops.error = {};
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/check`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			const paystack = PaystackPop.setup({
				key: import.meta.env.VITE_PAYSTACK_KEY,
				email: app.user.email,
				amount: resp.pay * 100,
				callback: (resp2) => {
					submit(resp2.reference);
				},
				onCancel: () => {
					module.open(Dialogue, {
						status: 400,
						title: 'Payment Canceled',
						messages: `The payment process was canceled`,
						button: [
							{
								name: 'Ok',
								icon: 'ok',
								fn: () => {
									module.close();
								}
							}
						]
					});
				}
			});
			paystack.openIframe();
		} else {
			ops.error = resp;
		}
	};

	const submit = async (reference) => {
		ops.error = {};

		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({
				reference,
				email_template_admin: email_template_admin.innerHTML.replace(/&amp;/g, '&'),
				email_template_user: email_template_user.innerHTML.replace(/&amp;/g, '&')
			})
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.cart_items = [];
			goto(`/orders/${resp.order.key}`);

			module.open(Dialogue, {
				status: 200,
				title: 'Successful',
				message: `Your order was placed successfully`,
				buttons: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							module.close();
						}
					}
				]
			});
		} else {
			ops.error = resp;
		}
	};

	let total = $derived.by(() => {
		let sum = ops.total_items() - (Number(ops.cart.discount_amount) || 0);
		if (ops.has_receiver()) {
			sum += Number(ops.cart.cost_delivery || 0);
		}
		return sum;
	});
</script>

<svelte:head>
	<script src="https://js.paystack.co/v2/inline.js"></script>
</svelte:head>

<div class="floater">
	<div class="floater_block">
		<div class="line space">
			<div class="total">Total Amount</div>
			<div class="cost">
				₦{total.toLocaleString()}
			</div>
		</div>

		<div class="checkout">
			<Button
				icon="cart"
				--button-color="white"
				--button-background-color="var(--cl1)"
				onclick={() => {
					if (!app.login) {
						module.open(Login);
					} else if (!ops.has_receiver()) {
						ops.status = 'Receiver';
						ops.error.error = 'Please provide receiver information before checkout';
						scroll('#Receiver');
					} else {
						make_payment();
					}
				}}
			>
				{#if !app.login}
					Login to
				{/if}
				Checkout
			</Button>
		</div>

		<Note note={ops.error.error} status="400" --note-margin-top="16px"></Note>
	</div>
</div>

<div bind:this={email_template_admin} style="display: none;">
	<Email_Admin order={ops.cart} items={app.cart_items} />
</div>
<div bind:this={email_template_user} style="display: none;">
	<Email_User order={ops.cart} items={app.cart_items} />
</div>

<style>
	.floater {
		position: sticky;
		bottom: var(--headerHeight);

		background-color: var(--bg1);
		border-top: 1px solid var(--bg2);
	}

	.floater_block {
		padding: 16px 24px;
		max-width: var(--mobileWidth);
		margin: auto;
	}

	.total {
		font-size: 0.8rem;
	}
	.cost {
		font-weight: 700;
		font-size: 1.2rem;
		color: var(--ft1);
	}

	.checkout {
		display: flex;
		justify-content: flex-end;
		margin-top: 16px;
	}
</style>
