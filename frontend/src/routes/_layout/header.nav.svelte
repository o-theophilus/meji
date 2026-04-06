<script>
	import { page } from '$app/state';
	import { Icon } from '$lib/macro';
</script>

<div class="nav">
	<div class="group">
		<!-- <a class:active={page.url.pathname == '/'} href="/">Home</a> -->
		<a class:active={page.url.pathname == '/about'} href="/about">About</a>
		<a class:active={page.url.pathname == '/partner'} href="/partner">Partner</a>
		<a class:active={page.url.pathname == '/blog'} href="/blog">Blog</a>
		<a class:active={page.url.pathname == '/contact'} href="/contact">Contact Us</a>
	</div>

	<div class="group shop">
		<a class:active={page.url.pathname == '/shop'} href="/shop">
			<Icon icon="shop{page.url.pathname == '/shop' ? '_active' : ''}"></Icon>
			Shop
		</a>
		<a class:active={page.url.pathname == '/save'} href="/save">
			<Icon icon="bookmark{page.url.pathname == '/save' ? '_active' : ''}"></Icon>
			Save
		</a>
		<a class:active={page.url.pathname == '/cart'} href="/cart">
			<Icon icon="cart{page.url.pathname == '/cart' ? '_active' : ''}"></Icon>
			Cart
		</a>
	</div>
</div>

<style>
	.nav {
		position: relative;

		display: none;
		align-items: center;
		justify-content: space-between;
		gap: 16px;

		max-width: var(--pageWidth);
		margin: auto;

		width: 100%;

		@media screen and (min-width: 580px) {
			display: flex;
		}

		&::before {
			content: '';
			position-anchor: --active;

			position: absolute;
			bottom: anchor(bottom);
			right: anchor(right);
			left: anchor(left);
			height: 4px;

			background-color: var(--cl1);
			border-radius: var(--toggle-border-radius, 4px);

			transition:
				right 0.2s ease-in-out,
				left 0.2s ease-in-out;
		}

		.group {
			display: flex;
			align-items: center;

			&.shop {
				display: none;
				@media screen and (min-width: 800px) {
					display: flex;
				}
			}
		}
	}

	a {
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		gap: 8px;

		height: var(--headerHeight);
		padding: 16px;
		text-decoration: none;
		color: var(--ft2);
		fill: var(--ft2);
		font-size: 0.8rem;

		transition: background-color 0.2s ease-in-out;

		&.active {
			anchor-name: --active;
			color: var(--ft1);
			fill: var(--ft1);
			background-color: var(--bg2);
		}

		&:hover {
			color: var(--ft1);
			fill: var(--ft1);
			background-color: var(--bg1);
		}
	}
</style>
