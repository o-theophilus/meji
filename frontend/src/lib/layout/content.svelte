<script>
	let { children } = $props();
</script>

<div class="bg">
	<section>
		{@render children()}
	</section>
</div>

<style>
	.bg {
		background-color: var(--content-background-color, var(--bg1));
	}
	section {
		max-width: var(--content-width, var(--mobileWidth));
		width: 100%;
		margin: auto;
		padding-left:  16px;
		padding-right:  16px;
		padding-top: var(--content-padding-top, 24px);
		padding-bottom: var(--content-padding-bottom, 24px);
		min-height: var(--content-height, calc(100vh - var(--headerHeight)));
		
		@media screen and (min-width: 580px) {
			& {
				padding-left:  24px;
				padding-right:  24px;
			}
		}
	}
</style>
