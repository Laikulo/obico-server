FROM bitnami/minideb:bookworm as npmyarn
RUN install_packages curl ca-certificates && \
    curl --fail -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash &&\
    bash -c 'source /root/.nvm/nvm.sh && nvm install 16.14.2' &&\
    mkdir /work
ENV PATH="/root/.nvm/versions/node/v16.14.2/bin:$PATH"
RUN npm install --global yarn
WORKDIR /work

FROM npmyarn as frontend_build
ADD . /work
#RUN --mount=type=bind,source=.,destination=/work,rw \
RUN \
    yarn install &&\
    yarn build --dest /out

FROM scratch as frontend_content
COPY --from=frontend_build /out/ /